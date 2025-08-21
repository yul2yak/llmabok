from typing import TypedDict


class CounterState(TypedDict):
    counter: int


from langgraph.graph import StateGraph, START, END


def test_increment():
    graph = StateGraph(CounterState)

    def increment(state: CounterState) -> CounterState:
        state["counter"] += 1
        return state

    graph.add_node("increment", increment)

    # graph.set_entry_point("increment")
    graph.add_edge(START, "increment")

    # graph.set_finish_point("increment")
    graph.add_edge("increment", END)

    app = graph.compile()
    response = app.invoke({"counter": 0})
    print(response)  # {'counter':1}

    with open("out/1-graph.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())


def test_assignment():
    class InputState(TypedDict):
        input: str

    class OutputState(TypedDict):
        output: str

    class PrivateState(TypedDict):
        private: str

    class OverallState(TypedDict):
        input: str
        output: str
        private: str

    def input_to_private(state: InputState) -> PrivateState:
        return {
            'private': f'{state["input"]} llm'
        }

    def private_to_output(state: PrivateState) -> OutputState:
        return {
            'output': f'{state['private']}. Nice to meet you!'
        }

    graph = StateGraph(
        OverallState,
        input_schema=InputState,
        output_schema=OutputState
    )
    graph.add_node("input_to_private", input_to_private)
    graph.add_node("private_to_output", private_to_output)

    graph.add_edge(START, "input_to_private")
    graph.add_edge("input_to_private", "private_to_output")
    graph.add_edge("private_to_output", END)

    app = graph.compile()
    response = app.invoke({
        'input': 'hello'
    })
    print(response)

    # with open("out/1-graph-assignment.png", "wb") as f:
    #     f.write(app.get_graph().draw_mermaid_png())


if __name__ == '__main__':
    test_assignment()
