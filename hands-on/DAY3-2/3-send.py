from typing import TypedDict, Annotated
import operator
from langgraph.types import Send
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    input: list[list[int]] | list[int]
    intermediate: Annotated[list[int], operator.add]
    output: int


def find_max(state: State) -> State:
    return {"intermediate": [max(state["input"])]}


def collect_max(state: State) -> State:
    return {"output": max(state["intermediate"])}


def test_send():
    graph = StateGraph(State)

    graph.add_node("find_max", find_max)
    graph.add_node("collect_max", collect_max)

    def distribute_max(state: State) -> list[Send]:
        return [
            Send('find_max', {'input': numbers})
            for numbers in state["input"]
        ]

    graph.add_conditional_edges(START, distribute_max, ["find_max"])
    graph.add_edge("find_max", "collect_max")
    graph.add_edge("collect_max", END)

    app = graph.compile()
    response = app.invoke({"input": [[4, 6, 5], [9, 2, 3], [7, 1, 8]]})
    print(response)

    with open("out/3-send.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())


if __name__ == "__main__":
    test_send()
