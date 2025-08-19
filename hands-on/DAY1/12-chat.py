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


# prompt = ChatPromptTemplate.from_messages([
#     ("system", "당신은 나의 친구입니다. 편안하게 대화해 주세요."),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "{user_input}")
# ])

# llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
# chain = prompt | llm
# print("대화를 시작하세요. 종료하려면 'exit'를 입력하세요.")
# history = []
# while True:
#     question = input("You: ")
#     if question.lower() == "exit":
#         break
#     history.append(("human", question))
#     response = chain.invoke({"history": history, 'user_input': question})
#     print("AI:", response.content)
#     history.append(("ai", response.content))


store = {}


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, storage_path: str, session_id: str):
        self.storage_path = storage_path
        self.session_id = session_id
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
        if not os.path.exists(os.path.join(storage_path, session_id)):
            with open(os.path.join(storage_path, session_id), "w") as f:
                f.write("[]")  # Initialize with an empty list

    @property
    def messages(self):
        with open(
            os.path.join(self.storage_path, self.session_id),
            "r",
            encoding="utf-8",
        ) as f:
            messages = json.loads(f.read())
        return messages_from_dict(messages)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)  # Existing messages
        all_messages.extend(messages)  # Add new messages

        serialized = [message_to_dict(message) for message in all_messages]
        # Can be further optimized by only writing new messages
        # using append mode.
        with open(os.path.join(self.storage_path, self.session_id), "w") as f:
            json.dump(messages, f)

    def clear(self):
        with open(os.path.join(self.storage_path, self.session_id), "w") as f:
            f.write("[]")


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        # store[session_id] = FileChatMessageHistory(
        #     storage_path='c:\\yul2ya\\llmabok\\hands-on\\chat_history.txt',
        #     session_id=session_id
        # )
        store[session_id] = InMemoryChatMessageHistory()
    return store.get(session_id)


prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 나의 친구입니다. 편안하게 대화해 주세요."),
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
    question = input("You: ")
    history.append(("human", question))
    if question.lower() in ("exit", "quit", "종료", "끝"):
        break
    response = chain.invoke(
        {"question": question, "history": history},
        config={"configurable": {"session_id": "1"}}
    )
    print("AI:", response.content)
    history.append(("ai", response.content))
