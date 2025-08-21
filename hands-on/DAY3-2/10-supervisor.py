import dotenv

dotenv.load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

add_agent = create_react_agent(llm, [add],
                               prompt="You are a math assistant. You can use tools to perform addition.",
                               name="add assistant"
                               )
multiply_agent = create_react_agent(llm, [multiply],
                                    prompt="You are a math assistant. You can use tools to perform addition.",
                                    name="multiply assistant"
                                    )
# pip install langgraph-supervisor
from langgraph_supervisor import create_supervisor

supervisor = create_supervisor([add_agent, multiply_agent],
                               model=llm, prompt="You manage a math assistant. Assign work to them."
                               ).compile()  # create_supervisorreturns StateGraph

