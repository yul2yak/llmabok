from langchain_core.messages import BaseMessage, messages_from_dict, message_to_dict
from typing import Sequence
import json
import os
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from click import prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import dotenv
dotenv.load_dotenv()

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store.get(session_id)


prompt = ChatPromptTemplate.from_messages([
    ("system", """당신은 주식 투자 교육 전문가 피터입니다.        
        주식 투자에 대한 기본 개념과 용어를 잘 알고 있어야 합니다.
        공격적인 투자 전략보다는 안정적이고 장기적인 투자 관점을 강조하세요.
        주식 시장의 기본 원리와 투자 전략에 대한 지식을 바탕으로 답변을 작성하세요.
        주식 투자에 대한 질문에 대해 친절하고 이해하기 쉽게 답변해 주세요.
        답변은 서로 대화하는 형식이 될 수 있도록 간결하고 짧게 가능하면 3줄 이내로 작성하세요.
        """),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
chain = RunnableWithMessageHistory(
    prompt | llm,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)
history = []
print("대화를 시작하세요. 종료하려면 'exit'를 입력하세요.")
while True:
    question = input("당신: ")
    history.append(("human", question))
    if question.lower() in ("exit", "quit", "종료", "끝"):
        break
    response = chain.invoke(
        {"question": question, "history": history},
        config={"configurable": {"session_id": "1"}}
    )
    print("투자 전문가:", response.content)
    history.append(("ai", response.content))
