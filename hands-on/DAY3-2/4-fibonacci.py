import operator
from typing import TypedDict, Annotated, Literal

from langgraph.constants import END
from langgraph.graph import StateGraph


class FibonacciState(TypedDict):
    N: int
    fibonacci: Annotated[list[int], operator.add]
    result: int

def test_fibonacci():
    graph = StateGraph(FibonacciState)
    graph.add_node('fibonacci', lambda s: dict(fibonacci=[0,1]))
    graph.add_node('calc_fibonacci', lambda s: dict(fibonacci=[s['fibonacci'][-2]+s['fibonacci'][-1]]))
    graph.add_node('exit_fibonacci', lambda s: dict(result=s['fibonacci'][s['N']]))
    graph.set_entry_point('fibonacci')
    graph.add_conditional_edges(
        'fibonacci',
        lambda s: 'exit' if s['N'] <= 1 else 'calc',
        {'exit':'exit_fibonacci', 'calc':'calc_fibonacci'}
    )
    graph.add_conditional_edges(
        'calc_fibonacci',
        lambda s: 'exit' if s['N'] < len(s['fibonacci']) else 'calc',
        {'exit': 'exit_fibonacci', 'calc': 'calc_fibonacci'}
    )
    graph.add_edge('fibonacci', 'calc_fibonacci')
    graph.add_edge('exit_fibonacci', END)

    app = graph.compile()
    response = app.invoke({"N":15})
    print(response)

    with open("out/4-fibonacci.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())

if __name__ == '__main__':
    test_fibonacci()