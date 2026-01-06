# API 修复说明

本文档说明了一些常见的 API 使用问题和修复方法。

## 问题 1: `system_prompt` 参数不存在

### 错误信息
```
TypeError: Agent.__init__() got an unexpected keyword argument 'system_prompt'
```

### 原因
Agno Agent 类不支持 `system_prompt` 参数。系统提示词需要通过其他方式设置。

### 解决方案

#### 方案 1: 在模型配置中设置（如果模型支持）

```python
from agno.models.openrouter import OpenRouter

model = OpenRouter(
    id="xiaomi/mimo-v2-flash:free",
    # 如果模型支持 system 参数
    # system="你是一个专业、友好的 AI 助手..."
)
```

#### 方案 2: 在首次对话时发送系统消息

```python
# 创建 Agent 后，在首次对话时发送系统消息
agent = Agent(...)

# 首次对话时包含系统提示
response = agent.run(
    "你是一个专业、友好的 AI 助手。你的职责是...",
    system=True  # 如果支持
)
```

#### 方案 3: 通过对话历史设置

在 Web 界面中，首次对话时发送系统提示词作为第一条消息。

### 已修复的文件
- ✅ `agent_with_local_mcp_sse.py` - 已移除 `system_prompt` 参数
- ✅ `agent_with_mcp.py` - 已移除 `system_prompt` 参数

## 问题 2: SSE 传输已弃用

### 警告信息
```
INFO SSE as a standalone transport is deprecated. Please use Streamable HTTP instead.
```

### 原因
SSE (Server-Sent Events) 作为独立传输协议已被弃用，推荐使用 `streamable-http`。

### 解决方案

#### 修改 MCP 工具配置

**之前（已弃用）:**
```python
mcp_tool = MCPTools(
    transport="sse",
    url="http://localhost:8001/mcp"
)
```

**现在（推荐）:**
```python
mcp_tool = MCPTools(
    transport="streamable-http",  # 使用 streamable-http
    url="http://localhost:8001/mcp"
)
```

#### 修改 MCP 服务器

MCP 服务器需要支持 HTTP POST 请求返回 JSON 响应，而不是 SSE 流。

**已更新的文件:**
- ✅ `mcp_server_example.py` - 已更新为支持 streamable-http
- ✅ `agent_with_local_mcp_sse.py` - 已改为使用 streamable-http

### 运行方式

**启动 MCP 服务器:**
```bash
# 使用 HTTP 模式（支持 streamable-http）
python mcp_server_example.py --mode http --port 8001
```

**配置 Agent:**
```python
mcp_tool = MCPTools(
    transport="streamable-http",
    url="http://localhost:8001/mcp"
)
```

## 问题 3: 其他可能不支持的参数

### 可能的问题参数
- `temperature` - 控制输出的随机性
- `max_tokens` - 最大输出 token 数

### 解决方案
如果这些参数导致错误，请从 Agent 配置中移除：

```python
# 如果报错，移除这些参数
agent = Agent(
    name="My Agent",
    model=model,
    db=db,
    tools=tools,
    add_history_to_context=True,
    markdown=True,
    # temperature=0.7,  # 如果报错，移除
    # max_tokens=2000,  # 如果报错，移除
)
```

如果需要在模型层面设置这些参数，可以在模型配置中设置：

```python
model = OpenRouter(
    id="xiaomi/mimo-v2-flash:free",
    temperature=0.7,  # 在模型配置中设置
    max_tokens=2000,  # 在模型配置中设置
)
```

## 正确的 Agent 配置示例

### 基础配置（推荐）

```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openrouter import OpenRouter
from agno.tools.mcp import MCPTools

# 配置模型
model = OpenRouter(id="xiaomi/mimo-v2-flash:free")

# 配置数据库
db = SqliteDb(db_file="agent.db")

# 配置 MCP 工具（使用 streamable-http）
mcp_tool = MCPTools(
    transport="streamable-http",
    url="http://localhost:8001/mcp"
)

# 创建 Agent（只使用支持的参数）
agent = Agent(
    name="My Agent",
    model=model,
    db=db,
    tools=[mcp_tool],
    add_history_to_context=True,
    markdown=True,
)
```

## 验证修复

运行以下命令验证修复：

```bash
# 1. 启动 MCP 服务器
python mcp_server_example.py --mode http --port 8001

# 2. 在另一个终端启动 Agent
python agent_with_local_mcp_sse.py
```

如果不再出现错误，说明修复成功。

## 参考

- Agno 官方文档: https://docs.agno.com
- MCP 协议文档: https://modelcontextprotocol.io
- 查看 `agno_agent.py` 了解正确的配置方式

