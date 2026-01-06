# Agent 实现完整指南

本指南将帮助你理解如何使用 Agno 框架实现一个完整的 Agent。

## 实现步骤概览

实现一个 Agent 通常包含以下步骤：

1. **导入必要的模块**
2. **配置模型 (Model)**
3. **配置数据库 (Database)**
4. **配置工具 (Tools)** - 可选
5. **创建 Agent**
6. **创建 AgentOS** - 可选
7. **运行 Agent**

## 详细步骤说明

### 步骤 1: 导入必要的模块

```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openrouter import OpenRouter
from agno.os import AgentOS
import os
from dotenv import load_dotenv
```

### 步骤 2: 配置模型

模型决定了 Agent 的 AI 能力。Agno 支持多种模型提供商：

- **OpenRouter**: 支持多种模型，包括免费模型
- **OpenAI**: GPT 系列模型
- **Anthropic**: Claude 系列模型
- **Google**: Gemini 系列模型

示例：
```python
# 使用 OpenRouter 的免费模型
model = OpenRouter(id="xiaomi/mimo-v2-flash:free")

# 或使用 OpenAI（需要 API key）
# from agno.models.openai import OpenAI
# model = OpenAI(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
```

### 步骤 3: 配置数据库

数据库用于存储 Agent 的对话历史和记忆，让 Agent 能够记住之前的对话。

```python
db = SqliteDb(db_file="agent.db")
```

### 步骤 4: 配置工具（可选）

工具可以让 Agent 执行特定操作，如：
- 调用 API
- 读取文件
- 执行代码
- 访问数据库

```python
# 示例：添加 MCP 工具
from agno.tools.mcp import MCPTools
tools = [MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")]
```

### 步骤 5: 创建 Agent

将所有组件组合起来创建 Agent：

```python
agent = Agent(
    name="我的 Agent",
    model=model,
    db=db,
    tools=tools,
    add_history_to_context=True,
    markdown=True,
)
```

### 步骤 6: 创建 AgentOS（可选）

AgentOS 可以管理多个 Agent，并提供 Web 界面：

```python
agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()
```

### 步骤 7: 运行 Agent

有两种运行方式：

**方式 1: 使用 AgentOS（推荐）**
```python
agent_os.serve(app="simple_agent_example:app", reload=True)
```
这会启动一个 Web 服务器，你可以通过浏览器访问 Agent。

**方式 2: 直接使用 Agent**
```python
response = agent.run("你好")
print(response.content)
```

## 完整示例

参考 `simple_agent_example.py` 文件，其中包含了完整的实现代码和详细注释。

## 运行示例

```bash
# 运行简单示例
python simple_agent_example.py

# 或运行原始示例
python agno_agent.py
```

## 常见配置选项

### Agent 配置选项

- `name`: Agent 的名称
- `model`: 使用的 AI 模型
- `db`: 数据库实例
- `tools`: 工具列表
- `add_history_to_context`: 是否将历史添加到上下文
- `markdown`: 是否支持 Markdown
- `system_prompt`: 自定义系统提示词
- `temperature`: 控制输出的随机性（0-1）
- `max_tokens`: 最大输出 token 数

### 模型选择建议

- **免费使用**: `xiaomi/mimo-v2-flash:free` (OpenRouter)
- **高质量对话**: `openai/gpt-4o-mini` 或 `anthropic/claude-3-haiku`
- **复杂任务**: `openai/gpt-4o` 或 `anthropic/claude-3-opus`

## 下一步

1. 尝试修改 `simple_agent_example.py` 中的配置
2. 添加自定义工具
3. 创建多个 Agent 并让它们协作
4. 自定义系统提示词以实现特定功能

## 参考资源

- Agno 官方文档: https://docs.agno.com
- 查看 `agno_agent.py` 了解更高级的配置

