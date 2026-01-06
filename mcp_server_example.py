"""
简单的 MCP 服务器示例
这个示例展示了如何创建一个本地的 MCP 服务器，供 Agent 使用

MCP (Model Context Protocol) 是一个标准协议，用于 AI 应用与外部工具之间的通信

支持两种运行模式：
1. stdio 模式：通过标准输入输出通信
2. HTTP 模式：通过 HTTP POST 返回 JSON（支持 streamable-http 协议）
"""

import json
import sys
from typing import Any, Dict, List
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn


class SimpleMCPServer:
    """
    一个简单的 MCP 服务器实现
    这个服务器提供了一些基础工具，如计算器、文本处理等
    """
    
    def __init__(self):
        self.tools = {
            "add": {
                "name": "add",
                "description": "将两个数字相加",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "第一个数字"},
                        "b": {"type": "number", "description": "第二个数字"}
                    },
                    "required": ["a", "b"]
                }
            },
            "multiply": {
                "name": "multiply",
                "description": "将两个数字相乘",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "第一个数字"},
                        "b": {"type": "number", "description": "第二个数字"}
                    },
                    "required": ["a", "b"]
                }
            },
            "uppercase": {
                "name": "uppercase",
                "description": "将文本转换为大写",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "要转换的文本"}
                    },
                    "required": ["text"]
                }
            }
        }
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理 MCP 请求"""
        method = request.get("method")
        params = request.get("params", {})
        
        # MCP 协议要求：首先处理 initialize 方法
        if method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "Simple MCP Server",
                    "version": "1.0.0"
                }
            }
        
        # 处理 tools/list 请求
        elif method == "tools/list":
            return {
                "tools": list(self.tools.values())
            }
        
        # 处理 tools/call 请求
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "add":
                print(f"add: {arguments}")
                result = arguments.get("a", 0) + arguments.get("b", 0)
                return {"content": [{"type": "text", "text": str(result)}]}
            
            elif tool_name == "multiply":
                print(f"multiply: {arguments}")
                result = arguments.get("a", 1) * arguments.get("b", 1)
                return {"content": [{"type": "text", "text": str(result)}]}
            
            elif tool_name == "uppercase":
                print(f"uppercase: {arguments}")
                text = arguments.get("text", "")
                result = text.upper()
                return {"content": [{"type": "text", "text": result}]}
            
            else:
                return {"error": {"code": -32601, "message": f"未知的工具: {tool_name}"}}
        
        # 处理其他可能的 MCP 方法
        elif method == "ping":
            return {"status": "ok"}
        
        else:
            return {"error": {"code": -32601, "message": f"未知的方法: {method}"}}
    
    def run_stdio(self):
        """使用 stdio 传输协议运行服务器"""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                request = json.loads(line.strip())
                request_id = request.get("id")
                result = self.handle_request(request)
                
                # 构建符合 JSON-RPC 2.0 规范的响应
                if "error" in result:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": result["error"]
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                
                print(json.dumps(response))
                sys.stdout.flush()
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if 'request' in locals() else None,
                    "error": {"code": -32603, "message": str(e)}
                }
                print(json.dumps(error_response))
                sys.stdout.flush()


# ========== SSE 模式支持 ==========
# 创建 FastAPI 应用
app = FastAPI(title="Simple MCP Server (SSE Mode)")

# 创建服务器实例
mcp_server = SimpleMCPServer()


@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """
    MCP 端点 - 支持 streamable-http
    接收 POST 请求，返回符合 JSON-RPC 2.0 规范的响应
    """
    try:
        # 读取请求体
        body = await request.body()
        request_data = json.loads(body.decode('utf-8'))
        
        # 获取请求 ID
        request_id = request_data.get("id")
        
        # 处理请求
        result = mcp_server.handle_request(request_data)
        
        # 检查是否有错误
        if "error" in result:
            # 如果返回的是错误，直接使用错误格式
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": result["error"]
            }
        else:
            # 正常响应：将结果包装在 result 字段中
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        
        # 返回 JSON 响应（streamable-http 模式）
        return JSONResponse(
            content=response,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        )
        
    except Exception as e:
        # 处理异常
        error_response = {
            "jsonrpc": "2.0",
            "id": request_data.get("id") if 'request_data' in locals() else None,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }
        return JSONResponse(
            content=error_response,
            status_code=500,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        )


@app.options("/mcp")
async def mcp_options():
    """处理 CORS 预检请求"""
    return {
        "status": "ok"
    }


@app.get("/")
async def root():
    """根路径，返回服务器信息"""
    return {
        "name": "Simple MCP Server",
        "mode": "streamable-http",
        "tools": list(mcp_server.tools.keys()),
        "endpoint": "/mcp"
    }


def run_http_server(host: str = "localhost", port: int = 8001):
    """运行 HTTP 模式的 MCP 服务器（支持 streamable-http）"""
    print(f"MCP 服务器已启动（HTTP 模式，支持 streamable-http）", file=sys.stderr)
    print(f"访问 http://{host}:{port} 查看服务器信息", file=sys.stderr)
    print(f"MCP 端点: http://{host}:{port}/mcp", file=sys.stderr)
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="运行 MCP 服务器")
    parser.add_argument(
        "--mode",
        choices=["stdio", "http"],
        default="stdio",
        help="运行模式：stdio 或 http（默认：stdio，http 模式支持 streamable-http）"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="HTTP 模式的服务器地址（默认：localhost）"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="HTTP 模式的服务器端口（默认：8001）"
    )
    
    args = parser.parse_args()
    
    if args.mode == "http":
        run_http_server(host=args.host, port=args.port)
    else:
        server = SimpleMCPServer()
        print("MCP 服务器已启动（stdio 模式）", file=sys.stderr)
        server.run_stdio()

