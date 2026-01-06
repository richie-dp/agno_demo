"""
带 MCP 工具和系统提示词的 Agent 实现示例
MCP (Model Context Protocol) 是一个标准协议，允许 Agent 访问外部工具和服务
"""

# ========== 步骤 1: 导入必要的模块 ==========
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openrouter import OpenRouter
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

import os
from dotenv import load_dotenv

# 加载环境变量（用于存储 API 密钥等敏感信息）
load_dotenv()


# ========== 步骤 2: 配置模型 (Model) ==========
model = OpenRouter(
    id="xiaomi/mimo-v2-flash:free",  # 使用免费模型
    # 如果需要使用其他模型，可以修改为：
    # id="openai/gpt-4o-mini"
    # api_key=os.getenv("OPENROUTER_API_KEY")
)


# ========== 步骤 3: 配置数据库 (Database) ==========
db = SqliteDb(
    db_file="agent_with_mcp.db"  # 数据库文件路径
)


# ========== 步骤 4: 配置 MCP 工具 (MCP Tools) ==========
# MCP (Model Context Protocol) 允许 Agent 访问外部工具和服务
# 
# MCP 工具配置方式：
# 1. 使用 streamable-http 传输协议连接远程 MCP 服务器
# 2. 使用 stdio 传输协议连接本地 MCP 服务器
# 3. 使用 sse 传输协议连接 Server-Sent Events 服务器

# 方式 1: 连接远程 MCP 服务器（使用 streamable-http）
mcp_tool = MCPTools(
    transport="streamable-http",  # 传输协议类型
    url="https://docs.agno.com/mcp"  # MCP 服务器的 URL
)

# 方式 2: 连接本地 MCP 服务器（使用 stdio）- 示例
# mcp_tool = MCPTools(
#     transport="stdio",
#     command="python",  # 运行命令
#     args=["path/to/mcp_server.py"]  # MCP 服务器脚本路径
# )

# 方式 3: 使用 SSE (Server-Sent Events) - 示例
# mcp_tool = MCPTools(
#     transport="sse",
#     url="http://localhost:8000/mcp"  # SSE 服务器 URL
# )

tools = [mcp_tool]


# ========== 步骤 5: 配置系统提示词 (System Prompt) ==========
# 注意：Agno Agent 不支持直接设置 system_prompt 参数
# 系统提示词可以通过以下方式设置：
# 1. 在模型配置中设置（如果模型支持 system 参数）
# 2. 在首次对话时发送系统消息
# 3. 通过其他 Agno 框架支持的方式
# 
# 以下是一个系统提示词的示例（仅供参考，实际使用时需要通过其他方式设置）：
# system_prompt = """你是一个专业、友好且高效的 AI 助手..."""


# ========== 步骤 6: 创建 Agent ==========
# 注意：Agent 不支持 system_prompt、temperature、max_tokens 等参数
# 这些参数如果报错，请移除
agent_with_mcp = Agent(
    name="带 MCP 工具的 Agent",  # Agent 的名称
    model=model,                  # 步骤 2 配置的模型
    db=db,                        # 步骤 3 配置的数据库
    tools=tools,                  # 步骤 4 配置的 MCP 工具
    # system_prompt 参数不存在，已移除
    
    # 其他配置选项：
    add_history_to_context=True,  # 将历史对话添加到上下文中
    markdown=True,                # 支持 Markdown 格式输出
    # temperature 和 max_tokens 可能也不支持，如果报错请移除
)


# ========== 步骤 7: 创建 AgentOS ==========
agent_os = AgentOS(agents=[agent_with_mcp])
app = agent_os.get_app()


# ========== 步骤 8: 运行 Agent ==========
if __name__ == "__main__":
    # 方式 1: 使用 AgentOS 运行（推荐，提供 Web 界面）
    print("正在启动 Agent 服务器...")
    print("访问 http://localhost:8000 来使用 Agent")
    agent_os.serve(app="agent_with_mcp:app", reload=True)
    
    # 方式 2: 直接使用 Agent（简单交互）
    # response = agent_with_mcp.run("你好，请介绍一下你自己，并告诉我你可以使用哪些工具")
    # print(response.content)

