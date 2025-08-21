from langchain_experimental.tools import PythonREPLTool
import dotenv
dotenv.load_dotenv()


def test_repl_tool():
    # https://python.langchain.com/docs/integrations/tools/python/
    tool = PythonREPLTool()
    response = tool.invoke("print(100 + 200)")
    print(response)


def test_using_repl_tool():
    from langchain.prompts import PromptTemplate
    prompt = PromptTemplate.from_template(
        """
        요청된 문제를 해결하는 파이썬 프로그램을 작성해줘
        # 요청
        {question} 
        # Do
        답변은 반드시 실행할 수 있는 python 코드 형태로 해줘
        # Example
        def sum(a:int, b:int)->int:
            return a+b
        print(sum(1,2))
        """
    )
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
    from langchain_core.output_parsers import StrOutputParser
    output_parser = StrOutputParser()
    tool = PythonREPLTool()
    from langchain.schema.runnable import RunnablePassthrough
    chain = dict(
        question=RunnablePassthrough()
    ) | prompt | llm | output_parser  # | tool
    response = chain.invoke('10개의 피보나치 수열 구해줘')
    print('llm 출력: ', response)
    response = tool.invoke(response)
    print('tool 결과: ', response)


if __name__ == '__main__':
    # test_repl_tool()
    test_using_repl_tool()
