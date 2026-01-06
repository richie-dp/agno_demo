# 使用 SSE 模式调用本地 MCP 服务器指南

本指南介绍如何使用 SSE (Server-Sent Events) 模式来调用自己写的 MCP 服务器工具。

## 什么是 SSE 模式？

SSE (Server-Sent Events) 是一种 HTTP 协议，允许服务器向客户端推送数据。在 MCP 中，SSE 模式通过 HTTP 服务器来提供 MCP 工具服务。

## 完整流程

### 步骤 1: 启动本地 MCP 服务器（SSE 模式）

首先，需要启动你的 MCP 服务器：

```bash
# 使用默认配置（localhost:8001）
python mcp_server_example.py --mode sse

# 或指定自定义地址和端口
python mcp_server_example.py --mode sse --host 0.0.0.0 --port 8001
```

启动成功后，你会看到：
```
MCP 服务器已启动（SSE 模式）
访问 http://localhost:8001 查看服务器信息
MCP 端点: http://localhost:8001/mcp
```

### 步骤 2: 验证 MCP 服务器

在浏览器中访问 `http://localhost:8001`，你应该能看到服务器信息，包括可用的工具列表。

### 步骤 3: 配置 Agent 使用 SSE 模式

在 Agent 代码中配置 MCP 工具：

```python
from agno.tools.mcp import MCPTools

mcp_tool = MCPTools(
    transport="sse",  # 使用 SSE 传输协议
    url="http://localhost:8001/mcp"  # 本地 MCP 服务器的 SSE 端点
)

tools = [mcp_tool]
```

### 步骤 4: 启动 Agent

```bash
python agent_with_local_mcp_sse.py
```

## 完整示例

参考以下文件：

1. **`mcp_server_example.py`** - MCP 服务器实现（支持 stdio 和 SSE 模式）
2. **`agent_with_local_mcp_sse.py`** - 使用 SSE 模式连接本地 MCP 服务器的 Agent

## 运行步骤

### 终端 1: 启动 MCP 服务器

```bash
python mcp_server_example.py --mode sse --port 8001
```

### 终端 2: 启动 Agent

```bash
python agent_with_local_mcp_sse.py
```

### 使用 Agent

1. 打开浏览器访问 `http://localhost:8000`
2. 与 Agent 对话，例如：
   - "请帮我计算 15 + 27"
   - "将 'hello world' 转换为大写"
   - "计算 5 乘以 8，然后将结果加上 10"

## MCP 服务器提供的工具

当前 `mcp_server_example.py` 提供了以下工具：

1. **add** - 加法运算
   - 参数：`a` (数字), `b` (数字)
   - 返回：两个数字的和

2. **multiply** - 乘法运算
   - 参数：`a` (数字), `b` (数字)
   - 返回：两个数字的积

3. **uppercase** - 文本转大写
   - 参数：`text` (字符串)
   - 返回：转换为大写的文本

## 添加自定义工具

要添加新工具，修改 `mcp_server_example.py`：

1. 在 `__init__` 方法的 `self.tools` 字典中添加工具定义
2. 在 `handle_request` 方法的 `tools/call` 分支中添加工具处理逻辑

示例：

```python
# 1. 添加工具定义
"subtract": {
    "name": "subtract",
    "description": "将两个数字相减",
    "inputSchema": {
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "被减数"},
            "b": {"type": "number", "description": "减数"}
        },
        "required": ["a", "b"]
    }
}

# 2. 添加工具处理逻辑
elif tool_name == "subtract":
    result = arguments.get("a", 0) - arguments.get("b", 0)
    return {"content": [{"type": "text", "text": str(result)}]}
```

修改后，重启 MCP 服务器即可使用新工具。

## 故障排除

### 问题 1: 连接失败

**错误**: `无法连接到 MCP 服务器`

**解决方案**:
- 确保 MCP 服务器正在运行
- 检查 URL 和端口是否正确
- 确保防火墙没有阻止连接

### 问题 2: 工具未找到

**错误**: `未知的工具: xxx`

**解决方案**:
- 检查工具名称是否正确
- 确保工具已在 `self.tools` 中定义
- 重启 MCP 服务器

### 问题 3: 端口被占用

**错误**: `Address already in use`

**解决方案**:
- 使用不同的端口：`--port 8002`
- 或停止占用端口的进程

### 问题 4: CORS 错误

如果遇到跨域问题，MCP 服务器已经配置了 CORS 头，应该不会有问题。如果仍有问题，检查：

- 服务器是否返回了正确的 CORS 头
- 浏览器控制台是否有错误信息

## 三种传输模式对比

| 模式 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| **stdio** | 本地开发、命令行工具 | 简单、直接 | 只能本地使用 |
| **sse** | Web 应用、远程访问 | 支持 HTTP、可远程访问 | 需要 HTTP 服务器 |
| **streamable-http** | 远程服务、云部署 | 标准 HTTP、易于部署 | 需要稳定的网络连接 |

## 下一步

1. 尝试添加更多自定义工具
2. 部署 MCP 服务器到云服务
3. 创建多个 Agent 使用同一个 MCP 服务器
4. 实现更复杂的工具逻辑

## 参考资源

- MCP 协议文档: https://modelcontextprotocol.io
- FastAPI 文档: https://fastapi.tiangolo.com
- 查看 `mcp_server_example.py` 了解完整实现
- 查看 `agent_with_local_mcp_sse.py` 了解 Agent 配置

