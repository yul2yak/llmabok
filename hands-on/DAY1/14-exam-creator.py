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
        주식 투자에 대한 이해도 평가용 객관식 문제를 제시하고, 답변이 오면 정답 여부를 판단하고 알려줍니다.
        왕초보, 초보, 초중급, 중급, 중상급, 상급, 전문가 등 7단계로 나누어 각 단계에 맞는 문제를 제시합니다.
        5문제 단위로 상대방의 수준을 평가하여 수준을 알려줍니다. 
        정답, 오답을 알려줄 때는 눈에 띄도록 이모티콘으로 강조해서 표현해주세요. 
        현재까지 맞춘 개수와 틀린 개수를 알려주고, 현재까지의 점수를 알려주세요.
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
    question = input("피평가자: ")
    history.append(("human", question))
    if question.lower() in ("exit", "quit", "종료", "끝"):
        break
    response = chain.invoke(
        {"question": question, "history": history},
        config={"configurable": {"session_id": "1"}}
    )
    print("평가자:", response.content)
    history.append(("ai", response.content))
