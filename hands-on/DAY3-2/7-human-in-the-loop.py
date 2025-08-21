import dotenv
from langgraph.constants import END

dotenv.load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

from typing import TypedDict


class State(TypedDict):
    subject: str
    story: str
    criticism: str


def generate_story(state: State) -> State:
    """Generate a revised story based on the provided state."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    prompt = f"""
            당신은 소설가입니다. 주제와 관련된 이야기를 만들어주세요. 
            이야기의 어떻게 흘러가는지에 대해 대략적인 스토리를 간략하게 만들어주세요. 
            ## 주제:
            {state['subject']}
            ## 이야기: 
            {state.get('story', '')}
            ## 비평:
            {state.get('criticism', '')}
        """
    response = llm.invoke(prompt)
    return {"story": response.content}


def user_critic(state: State) -> State:
    criticism = input(f"비평을 입력하세요. : ")
    return {"criticism": criticism}


from langgraph.graph import StateGraph


def test_human_in_the_loop():
    graph = StateGraph(State)
    graph.add_node("generate_story", generate_story)
    graph.add_node("user_critic", user_critic)
    graph.set_entry_point("generate_story")
    graph.add_edge("generate_story", "user_critic")

    def check_user_criticism(state: State):
        if state["criticism"] != "": return "revise"
        return "exit"

    graph.add_conditional_edges(
        "user_critic",
        check_user_criticism,
        {"revise": "generate_story", "exit": END}
    )
    app = graph.compile()
    result = app.invoke({"subject": "고양이의 보은"})
    print(result)


if __name__ == "__main__":
    test_human_in_the_loop()
