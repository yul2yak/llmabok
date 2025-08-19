from datetime import datetime
from itertools import chain
from urllib import response
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import dotenv
dotenv.load_dotenv()


# country = input("국가를 입력하세요: ")
prompt = PromptTemplate.from_template("{country}의 수도는?")
print(prompt)

result = prompt.invoke({"country": "한국"})
print(result)  # text='한국의 수도는?'

result = prompt.invoke({"country": "일본"})
print(result)  # text='일본의 수도는?'

llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

# chain = prompt | llm
# response = chain.invoke("중국")
# print(response)  # text='중국의 수도는 베이징입니다.'

# seq = RunnableSequence(prompt, llm)
# response = seq.invoke({"country": "미국"})
# print(response)  # text='미국의 수도는 워싱턴 D.C.입니다.'

prompt = PromptTemplate.from_template("생일이 {date}인 유명인을 {n}명 알려줘.")
# chain = prompt | llm
# today = datetime.now().strftime("%m월 %d일")
# response = chain.invoke({"date": today, "n": 3})
# print(response.content)

prompt = prompt.partial(date=datetime.now().strftime("%m월 %d일"))
prompt.pretty_print()
result = prompt.invoke({"n": 3})
print(result)  # text='생일이 10월 04일인 유명인을 3명 알려줘.'
result = prompt.invoke({"date": "8월 13일", "n": 5})
print(result)  # text='생일이 8월 13일인 유명인을 5명 알려줘.'

prompt = PromptTemplate(
    template="오늘은 {date}입니다. {n}명의 유명인의 생일을 알려주세요.",
    input_variables=['n'],
    partial_variables={'date': datetime.now().strftime("%m월 %d일")}
)
print(prompt.invoke({"n": 2}))
print(prompt.invoke({"date": "6월 20일", "n": 3}))
