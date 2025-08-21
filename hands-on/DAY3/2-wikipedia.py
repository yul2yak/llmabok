from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


def test_wikipedia():
    '''https://python.langchain.com/docs/integrations/tools/wikipedia'''
    tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

    # response = tool.invoke("한국의 대통령은?")
    response = tool.invoke({"query": "한국의 대통령은?"})
    print(response)


if __name__ == "__main__":
    test_wikipedia()
