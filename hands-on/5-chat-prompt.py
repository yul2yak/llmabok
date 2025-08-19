from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import dotenv
dotenv.load_dotenv()

print('-- 테디 --')
prompt = ChatPromptTemplate.from_messages(
    [  # (role, message)
        ("system", "당신은 친절한 AI 어시스턴트입니다. 당신의 이름은 {name} 입니다."),
        ("human", "반가워요!"),
        ("ai", "안녕하세요! 무엇을 도와드릴까요?"),
        ("human", "{user_input}"),
    ]
)
prompt.pretty_print()
args = {"name": "테디", "user_input": "당신의 이름은 무엇입니까?"}
prompt_val = prompt.invoke(args)

print(prompt_val)

llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
chain = prompt | llm
response = chain.invoke(args)
print(response.content)

print('-- 대화 요약 --')
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 요약 전문 AI 어시스턴트 야커입니다."),
    MessagesPlaceholder(variable_name="conversation"),
    ("human", "지금까지의 대화를 {word_count} 단어로 요약해 주세요."),

])

conversation = [
    ("human", "안녕하세요! 저는 오늘 새로 입사한 테디 입니다. 만나서 반갑습니다."),
    ("ai", "반가워요! 앞으로 잘 부탁 드립니다."),
]
prompt_val = prompt.invoke({
    "word_count": 5,
    "conversation": conversation
})

print(prompt_val)

chain = prompt | llm
response = chain.invoke({
    "word_count": 5,
    "conversation": conversation
})
print(response.content)
