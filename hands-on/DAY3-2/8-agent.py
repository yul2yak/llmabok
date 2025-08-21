import dotenv
from langgraph.constants import END

dotenv.load_dotenv()

from langchain_core.tools import tool
from langgraph.graph import MessagesState, StateGraph
from langchain_core.messages import ToolMessage


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


def test_agent():
    tools = [add, multiply]
    tools_by_name = {tool.name: tool for tool in tools}
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    from langgraph.prebuilt import create_react_agent
    agent = create_react_agent(llm, tools=[add, multiply])

    def llm_call(state: MessagesState):
        """LLM decides whether to call a tool or not"""
        response = agent.invoke(state["messages"])
        print(response)
        return {"messages": [response]}

    def tool_node(state: MessagesState):
        """Performs the tool call"""
        messages = []
        for tool_call in state["messages"][-1].tool_calls:
            tool = tools_by_name[tool_call["name"]]
            response = tool.invoke(tool_call["args"])
            messages.append(ToolMessage(content=response,
                                        tool_call_id=tool_call["id"]))
        return {"messages": messages}

    def should_continue(state: MessagesState):
        """Decide if we should continue the loop or stop
        based upon whether the LLM made a tool call"""
        if state["messages"][-1].tool_calls: return "tool"
        return "exit"

    graph = StateGraph(MessagesState)
    graph.add_node('llm_call', llm_call)
    graph.add_node('tool_node', tool_node)
    graph.set_entry_point('llm_call')
    graph.add_conditional_edges(
        "llm_call",
        should_continue,
        {"tool": "tool_node", "exit": END},
    )

    app = graph.compile()
    result = app.invoke({
        'messages': ['3 더하기 4는?'],
    })
    print(result)

    # from langchain_core.messages import HumanMessage
    # response = agent.invoke({"messages": [HumanMessage(content="3 더하기 4는?")]})
    # for m in response["messages"]:
    #     m.pretty_print()

