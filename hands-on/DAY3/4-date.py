import dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool

dotenv.load_dotenv()

from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate, MessagesPlaceholder

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage


def test_date():
    prompt = PromptTemplate.from_template("오늘은 {today}입니다. {question}")

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    chain = prompt | llm

    today = f'{datetime.today():%Y년 %m월 %d일}'

    response = chain.invoke(dict(today=today, question='모레는 무슨 요일인가요?'))
    print(response.content)


@tool
def get_today():
    """
    오늘 날짜를 반환하는 도구
    날짜 형식: YYYY년 MM월 DD일
    """
    return f'{datetime.today():%Y년 %m월 %d일}'


def test_date_with_tool():
    messages = [
        SystemMessage("오늘 날짜와 요일은 'get_today' 도구를 사용하여 알 수 있습니다."),
        HumanMessage('모레는 무슨 요일인가요?'),
    ]
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    llm_with_tools = llm.bind_tools([get_today])
    chain = llm_with_tools
    ai_message = chain.invoke(messages)
    print(ai_message)
    messages.append(ai_message)

    for tool_call in ai_message.tool_calls:
        if tool_call["name"] == "get_today":
            messages.append(get_today.invoke(tool_call))
    ai_message = chain.invoke(messages)
    print(ai_message)
    messages.append(ai_message)

    for message in messages:
        message.pretty_print()

def test_date_with_agent():
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(
            "당신은 도구를 사용하는 AI입니다. "            
            "오늘 날짜와 요일은 'get_today' 도구를 사용해서 알 수 있습니다."
            "사용자의 질문에 대해 직접 계산하여 최종 답변을 출력하세요."
        ),
        HumanMessagePromptTemplate.from_template('{question}'), #⭐
        MessagesPlaceholder(variable_name='agent_scratchpad'),
    ])
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    agent = create_tool_calling_agent(llm, [get_today], prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[get_today])
    response = agent_executor.invoke(dict(question='다음주 월요일은 몇일이야?'))
    print(response)