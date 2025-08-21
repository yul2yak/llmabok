from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool


def test_add():
    @tool  # (parse_docstring=True)
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        # """
        # Add two numbers.

        # Args:
        #     a (int): the left operand.
        #     b (int): the right operand.

        # Returns:
        #     The sum of the two operands.
        # """
        return a + b

    print(type(add))
    print(add.name)
    print(add.description)
    print(add.args)

    # response = add.invoke({"a": 2, "b": 3})
    response = add.invoke(dict(a=2, b=3))
    print(response)


def test_runnable_lambda():
    inc = RunnableLambda(lambda input: input['x']+1)
    inc_tool = inc.as_tool(
        name='increment', description='Increment a number by 1')
    print(type(inc_tool))
    print(inc_tool.name)
    print(inc_tool.description)
    response = inc_tool.invoke(dict(x=1))
    print(response)


def test_multiply():
    @tool(parse_docstring=True)
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers.

        Args:
            a: the left operand.
            b: the right operand.
        """
        return a*b

    print(multiply.name)
    print(multiply.description)
    print(multiply.args)


if __name__ == '__main__':
    test_add()
    test_runnable_lambda()
    test_multiply()
