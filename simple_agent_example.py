"""
简单的 Agent 实现示例
这个文件展示了如何使用 Agno 框架创建一个完整的 Agent 的步骤
"""

# ========== 步骤 1: 导入必要的模块 ==========
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openrouter import OpenRouter
from agno.os import AgentOS

import os
from dotenv import load_dotenv

# 加载环境变量（用于存储 API 密钥等敏感信息）
load_dotenv()


# ========== 步骤 2: 配置模型 (Model) ==========
# 模型决定了 Agent 使用的 AI 能力
# 这里使用 OpenRouter 提供的免费模型
model = OpenRouter(
    id="xiaomi/mimo-v2-flash:free",  # 模型 ID
    # 如果需要使用其他模型，可以修改为：
    # id="openai/gpt-4o-mini"  # 或其他支持的模型
    # api_key=os.getenv("OPENROUTER_API_KEY")  # 如果使用需要 API key 的模型
)


# ========== 步骤 3: 配置数据库 (Database) ==========
# 数据库用于存储 Agent 的对话历史和记忆
# SqliteDb 是一个轻量级的本地数据库
db = SqliteDb(
    db_file="simple_agent.db"  # 数据库文件路径
    # 如果文件不存在，会自动创建
)


# ========== 步骤 4: 配置工具 (Tools) - 可选 ==========
# 工具可以让 Agent 执行特定的操作
# 这里暂时不添加工具，创建一个基础 Agent
# 如果需要添加工具，可以这样做：
# from agno.tools.mcp import MCPTools
# tools = [MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")]
tools = []  # 空列表表示不使用任何工具


# ========== 步骤 5: 创建 Agent ==========
simple_agent = Agent(
    name="简单示例 Agent",  # Agent 的名称
    model=model,            # 步骤 2 配置的模型
    db=db,                  # 步骤 3 配置的数据库
    tools=tools,            # 步骤 4 配置的工具（可选）
    
    # 以下是一些常用的配置选项：
    add_history_to_context=True,  # 是否将历史对话添加到上下文中
    markdown=True,                # 是否支持 Markdown 格式输出
    # system_prompt="你是一个友好的助手",  # 自定义系统提示词（可选）
)


# ========== 步骤 6: 创建 AgentOS (可选) ==========
# AgentOS 可以管理多个 Agent，并提供 Web 界面
# 如果只需要单个 Agent，可以跳过这一步，直接使用 Agent
agent_os = AgentOS(agents=[simple_agent])
app = agent_os.get_app()


# ========== 步骤 7: 运行 Agent ==========
if __name__ == "__main__":
    # 方式 1: 使用 AgentOS 运行（推荐，提供 Web 界面）
    agent_os.serve(app="simple_agent_example:app", reload=True)
    
    # 方式 2: 直接使用 Agent（简单交互）
    # response = simple_agent.run("你好，请介绍一下你自己")
    # print(response.content)

