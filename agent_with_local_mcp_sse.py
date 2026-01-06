"""
使用 streamable-http 模式连接本地 MCP 服务器的 Agent 示例
这个示例展示了如何通过 streamable-http 模式调用自己写的 MCP 服务器工具
"""

# ========== 步骤 1: 导入必要的模块 ==========
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openrouter import OpenRouter
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


# ========== 步骤 2: 配置模型 ==========
# 注意：系统提示词可以通过在对话开始时发送系统消息来设置
# 或者通过模型的 system 参数（如果模型支持）
# 
# 重要：如果遇到 401 错误 "User not found"，需要设置 OpenRouter API key
# 1. 访问 https://openrouter.ai/ 注册并获取 API key
# 2. 在 .env 文件中添加: OPENROUTER_API_KEY=your_api_key_here
# 3. 取消下面的注释并设置 api_key
model = OpenRouter(
    id="xiaomi/mimo-v2-flash:free",
    # 如果遇到 401 错误，取消下面的注释并设置 API key
    # api_key=os.getenv("OPENROUTER_API_KEY"),
    # 如果模型支持，可以在这里设置系统提示词
    # system="你是一个专业、友好的 AI 助手..."
)


# ========== 步骤 3: 配置数据库 ==========
db = SqliteDb(
    db_file="agent_local_mcp_sse.db"
)


# ========== 步骤 4: 配置本地 MCP 工具（streamable-http 模式） ==========
# 使用 streamable-http 模式连接本地 MCP 服务器
# 确保 mcp_server_example.py 已经以 HTTP 模式运行（见下方运行说明）
mcp_tool = MCPTools(
    transport="streamable-http",  # 使用 streamable-http 传输协议（推荐，SSE 已弃用）
    url="http://localhost:8001/mcp"  # 本地 MCP 服务器的 HTTP 端点
)

tools = [mcp_tool]


# ========== 步骤 5: 配置模型（包含系统提示词） ==========
# 注意：Agno Agent 不支持直接设置 system_prompt 参数
# 系统提示词可以通过模型配置或其他方式设置
# 这里我们通过模型的 system 参数来设置（如果模型支持）


# ========== 步骤 6: 创建 Agent ==========
# 注意：Agent 不支持 system_prompt 参数
# 系统提示词可以通过以下方式设置：
# 1. 在模型配置中设置（如果模型支持）
# 2. 在首次对话时发送系统消息
# 3. 通过其他 Agno 框架支持的方式
agent = Agent(
    name="本地 MCP 工具 Agent (HTTP)",
    model=model,
    db=db,
    tools=tools,
    # system_prompt 参数不存在，已移除
    add_history_to_context=True,
    markdown=True,
    # temperature 和 max_tokens 可能也不支持，如果报错请移除
)


# ========== 步骤 7: 创建 AgentOS ==========
agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()


# ========== 步骤 8: 运行 Agent ==========
if __name__ == "__main__":
    print("=" * 60)
    print("重要提示：")
    print("1. 请先启动本地 MCP 服务器（HTTP 模式）：")
    print("   python mcp_server_example.py --mode http --port 8001")
    print("2. 然后启动此 Agent")
    print("=" * 60)
    print()
    
    print("正在启动 Agent 服务器...")
    print("访问 http://localhost:8000 来使用 Agent")
    print()
    
    agent_os.serve(app="agent_with_local_mcp_sse:app", reload=True)
    
    # 方式 2: 直接使用 Agent（简单交互）
    # response = agent.run("请帮我计算 15 + 27，然后将结果乘以 3")
    # print(response.content)

