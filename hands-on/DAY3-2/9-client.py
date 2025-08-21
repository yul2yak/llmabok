import asyncio

from langgraph_sdk import get_client

client = get_client(url="http://localhost:2024")

from langchain_core.messages import HumanMessage


async def main():
    response = await client.runs.wait(
        None,  # Threadless run
        "agent",  # Name of assistant. Defined in langgraph.json.
        input={"messages": [HumanMessage("2에 3을 더한 결과에 5를 곱하면?")]}
    )

    print(response["messages"][-1]["content"])


asyncio.run(main())
