# MCP 初始化错误修复

## 错误 1: `Failed to initialize MCP toolkit: 未知的方法: initialize`

### 问题描述
MCP 工具初始化失败，因为 MCP 服务器没有实现 `initialize` 方法。

### 原因
MCP (Model Context Protocol) 协议要求在建立连接时，客户端必须先调用 `initialize` 方法来初始化连接。我们的 MCP 服务器缺少这个方法。

### 解决方案
已在 `mcp_server_example.py` 中添加了 `initialize` 方法处理：

```python
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
```

### 修复状态
✅ 已修复 - `mcp_server_example.py` 现在支持 `initialize` 方法

---

## 错误 2: `API status error: User not found. (401)`

### 问题描述
OpenRouter API 返回 401 错误，提示 "User not found."

### 可能的原因
1. **需要 API Key**: 即使使用免费模型，某些情况下仍需要 OpenRouter API key
2. **模型 ID 错误**: 模型 ID 可能不正确或已变更
3. **认证配置问题**: API key 未正确配置

### 解决方案

#### 方案 1: 添加 OpenRouter API Key

1. 访问 [OpenRouter](https://openrouter.ai/) 注册账号
2. 获取 API key
3. 在 `.env` 文件中添加：

```bash
OPENROUTER_API_KEY=your_api_key_here
```

4. 在代码中使用：

```python
from agno.models.openrouter import OpenRouter
import os
from dotenv import load_dotenv

load_dotenv()

model = OpenRouter(
    id="xiaomi/mimo-v2-flash:free",
    api_key=os.getenv("OPENROUTER_API_KEY")  # 添加 API key
)
```

#### 方案 2: 尝试其他免费模型

如果当前模型不可用，可以尝试其他免费模型：

```python
# 选项 1: 使用其他免费模型
model = OpenRouter(
    id="google/gemini-flash-1.5-8b:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# 选项 2: 使用 OpenAI 兼容的模型（需要 API key）
from agno.models.openai import OpenAI
model = OpenAI(
    id="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)
```

#### 方案 3: 检查模型 ID

确认模型 ID 是否正确，可以访问 OpenRouter 的模型列表：
https://openrouter.ai/models

### 验证步骤

1. **检查 MCP 服务器是否正常运行**:
   ```bash
   python mcp_server_example.py --mode http --port 8001
   ```

2. **检查 API key 是否正确设置**:
   ```bash
   # 在 Python 中测试
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENROUTER_API_KEY'))"
   ```

3. **测试模型连接**:
   创建一个简单的测试脚本验证模型是否可用

### 修复后的完整配置示例

```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openrouter import OpenRouter
from agno.tools.mcp import MCPTools
import os
from dotenv import load_dotenv

load_dotenv()

# 配置模型（带 API key）
model = OpenRouter(
    id="xiaomi/mimo-v2-flash:free",
    api_key=os.getenv("OPENROUTER_API_KEY")  # 确保设置了 API key
)

# 配置数据库
db = SqliteDb(db_file="agent.db")

# 配置 MCP 工具
mcp_tool = MCPTools(
    transport="streamable-http",
    url="http://localhost:8001/mcp"
)

# 创建 Agent
agent = Agent(
    name="My Agent",
    model=model,
    db=db,
    tools=[mcp_tool],
    add_history_to_context=True,
    markdown=True,
)
```

## 总结

1. ✅ **MCP initialize 方法** - 已修复
2. ⚠️ **API 认证问题** - 需要配置 OpenRouter API key

重启 MCP 服务器和 Agent 后，第一个错误应该已经解决。如果仍有 API 错误，请按照上述方案配置 API key。

