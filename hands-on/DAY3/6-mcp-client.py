import asyncio
from dotenv import load_dotenv

load_dotenv()

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    # {
    #     "math": {
    #         "command": "python",
    #         "args": ["5-mcp-server.py"],
    #         "transport": "stdio",
    #     }
    # }
    {
        "math": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:8000/mcp"
        }
    }
)


async def test_mcp_client():
    tools = await client.get_tools()  # asynchronous call to get tools

    for tool in tools:
        print(tool.name, tool.description)


async def test_ai_with_mcp_tool():
    tools = await client.get_tools()
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(
            "당신은 도구를 사용하는 AI입니다. "
            "사용자의 질문에 대해 직접 계산하여 최종 답변을 출력하세요."
        ),
        ('human', '{question}'),
        MessagesPlaceholder(variable_name='agent_scratchpad'),
    ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    response = await agent_executor.ainvoke(dict(question='2와 3을 더하면 얼마인가요?'))
    print(response)


async def test_ai_with_mcp_langgraph():
    tools = await client.get_tools()
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    from langgraph.prebuilt import create_react_agent
    agent = create_react_agent(llm, tools)
    response = await agent.ainvoke(
        dict(messages=[
            ('system', '툴을 사용해서 사용자 질문에 답변하세요'),
            ('user', '2 + 3 * 5 는?')
        ])
    )
    for message in response['messages']:
        message.pretty_print()

async def test_filesystem_tool():
    client = MultiServerMCPClient(
        {
            "math": {
                ""
            }
        }
    )

if __name__ == "__main__":
    # asyncio.run(test_mcp_client())
    # asyncio.run(test_ai_with_mcp_tool()) #error
    asyncio.run(test_ai_with_mcp_langgraph())
