# MCP 工具使用指南

本指南介绍如何在 Agno Agent 中使用 MCP (Model Context Protocol) 工具。

## 什么是 MCP？

MCP (Model Context Protocol) 是一个标准协议，允许 AI 应用（如 Agent）与外部工具和服务进行通信。通过 MCP，Agent 可以：

- 访问外部 API
- 执行系统操作
- 读取文件和数据
- 调用其他服务

## MCP 工具配置方式

### 方式 1: 使用 streamable-http 连接远程 MCP 服务器

这是最简单的方式，适用于连接已部署的远程 MCP 服务器：

```python
from agno.tools.mcp import MCPTools

mcp_tool = MCPTools(
    transport="streamable-http",
    url="https://docs.agno.com/mcp"  # MCP 服务器的 URL
)
```

### 方式 2: 使用 stdio 连接本地 MCP 服务器

适用于运行本地的 MCP 服务器脚本：

```python
from agno.tools.mcp import MCPTools

mcp_tool = MCPTools(
    transport="stdio",
    command="python",  # 运行命令
    args=["path/to/mcp_server.py"]  # MCP 服务器脚本路径
)
```

### 方式 3: 使用 SSE (Server-Sent Events)

适用于使用 SSE 协议的 MCP 服务器：

```python
from agno.tools.mcp import MCPTools

mcp_tool = MCPTools(
    transport="sse",
    url="http://localhost:8000/mcp"  # SSE 服务器 URL
)
```

## 创建自定义 MCP 服务器

你可以创建自己的 MCP 服务器来提供自定义工具。参考 `mcp_server_example.py` 文件，其中包含了一个简单的 MCP 服务器实现。

### MCP 服务器基本结构

一个 MCP 服务器需要：

1. **工具定义**: 定义服务器提供的工具及其参数
2. **请求处理**: 处理来自 Agent 的工具调用请求
3. **响应格式**: 返回符合 MCP 协议格式的响应

### 示例：简单的计算器 MCP 服务器

```python
# mcp_server_example.py 中包含了完整的实现
# 该服务器提供了以下工具：
# - add: 加法运算
# - multiply: 乘法运算
# - uppercase: 文本转大写
```

## 系统提示词 (System Prompt)

系统提示词定义了 Agent 的角色、能力和行为准则。这是非常重要的配置。

### 为什么需要系统提示词？

- **定义角色**: 告诉 Agent 它是什么，应该扮演什么角色
- **设定行为**: 指导 Agent 如何响应用户请求
- **工具使用**: 告诉 Agent 如何使用可用的工具
- **输出格式**: 定义 Agent 的输出风格和格式

### 系统提示词最佳实践

1. **明确角色**: 清楚地定义 Agent 的角色
   ```
   你是一个专业的数据分析助手。
   ```

2. **说明能力**: 列出 Agent 可以做什么
   ```
   你可以：
   - 分析数据
   - 生成报告
   - 使用 MCP 工具访问外部数据
   ```

3. **行为准则**: 设定 Agent 的行为规范
   ```
   你的行为准则：
   - 始终以用户为中心
   - 优先使用工具完成任务
   - 如果工具失败，提供替代方案
   ```

4. **工具说明**: 说明如何使用工具
   ```
   当用户需要计算时，使用 add 或 multiply 工具。
   当用户需要处理文本时，使用 uppercase 工具。
   ```

## 完整示例

参考 `agent_with_mcp.py` 文件，其中包含：

1. ✅ MCP 工具配置（使用 streamable-http）
2. ✅ 系统提示词配置
3. ✅ 完整的 Agent 创建流程
4. ✅ 详细的注释说明

## 运行示例

```bash
# 运行带 MCP 工具的 Agent
python agent_with_mcp.py

# 如果需要测试本地 MCP 服务器
python mcp_server_example.py
```

## 常见问题

### Q: 如何知道 MCP 服务器提供了哪些工具？

A: Agent 会自动发现 MCP 服务器提供的工具。你也可以在系统提示词中说明可用的工具。

### Q: MCP 工具调用失败怎么办？

A: 在系统提示词中告诉 Agent 如何处理工具失败的情况，比如：
```
如果工具执行失败，向用户说明情况并提供替代方案。
```

### Q: 可以同时使用多个 MCP 工具吗？

A: 可以！在 `tools` 列表中添加多个 `MCPTools` 实例：

```python
tools = [
    MCPTools(transport="streamable-http", url="https://server1.com/mcp"),
    MCPTools(transport="streamable-http", url="https://server2.com/mcp"),
]
```

### Q: 如何调试 MCP 工具？

A: 
1. 检查 MCP 服务器是否正常运行
2. 验证 URL 或命令是否正确
3. 查看 Agent 的日志输出
4. 在系统提示词中要求 Agent 报告工具执行情况

## 下一步

1. 尝试修改 `agent_with_mcp.py` 中的系统提示词
2. 创建自己的 MCP 服务器（参考 `mcp_server_example.py`）
3. 连接多个 MCP 服务器
4. 自定义工具和功能

## 参考资源

- MCP 官方文档: https://modelcontextprotocol.io
- Agno 文档: https://docs.agno.com
- 查看 `agent_with_mcp.py` 了解完整实现

