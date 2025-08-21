from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, Send


class CounterState(TypedDict):
    counter: int


class UserInputState(TypedDict):
    user_input: str


def test_conditional():
    graph = StateGraph(CounterState)

    def get_user_input(state: CounterState) -> UserInputState:
        print(f"Counter value: {state['counter']}")
        user_input = input("Input (+, -, .): ")
        return {
            "user_input": user_input,
        }

    graph.add_node('get_user_input', get_user_input)
    graph.add_node('decrement', lambda state: {'counter': state['counter'] - 1})
    graph.add_node('increment', lambda state: {'counter': state['counter'] + 1})
    graph.add_edge(START, 'get_user_input')

    def check_user_input(state: UserInputState):
        actions = {'+': 'increment', '-': 'decrement'}
        return actions.get(state['user_input'], 'exit')

    graph.add_conditional_edges(
        'get_user_input',
        check_user_input,
        {'increment': 'increment', 'decrement': 'decrement', 'exit': END},
    )
    graph.add_edge('increment', 'get_user_input')
    graph.add_edge('decrement', 'get_user_input')

    app = graph.compile()
    response = app.invoke({'counter': 0})
    print(response)

    with open("out/2-conditional.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())


def test_conditional_with_command():
    graph = StateGraph(CounterState)

    def get_user_input(state: CounterState) -> Command:
        print(f"Counter value: {state['counter']}")
        user_input = input("Input (+, -, .): ")
        actions = {
            '+': Command(goto='increment'),
            '-': Command(goto='decrement')
        }
        return actions.get(user_input, Command(goto=END))

    graph.add_node('get_user_input', get_user_input)
    graph.add_node(
        'decrement',
        lambda state: Command(
            update={'counter': state['counter'] - 1},
            goto='get_user_input'
        )
    )
    graph.add_node(
        'increment',
        lambda state: Command(
            update={'counter': state['counter'] + 1},
            goto='get_user_input'
        )
    )
    graph.set_entry_point('get_user_input')
    graph.add_edge('increment', 'get_user_input')
    graph.add_edge('decrement', 'get_user_input')

    app = graph.compile()
    response = app.invoke({'counter': 0})
    print(response)

    with open("out/2-conditional-command.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())

if __name__ == "__main__":
    test_conditional()
    test_conditional_with_command()
