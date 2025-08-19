from http import client
import os
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model
import dotenv
dotenv.load_dotenv()

# llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

# llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
# client = genai.Client()
# file = client.files.upload(file='c:\\yul2ya\\llmabok\\data\\AI 에이전트 동향.pdf')
# cache = client.caches.create(
#     model="gemini-2.5-flash",
#     config=genai.types.CreateCachedContentConfig(contents=[file])
# )

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     cached_content=cache.name,
# )

# response = llm.invoke('보고서의 내용을 요약해줘')
# print(response.content)

client = genai.Client()
image = client.files.upload(file='c:\\yul2ya\\llmabok\\data\\일출.jpg')

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[image, "이 사진에 대해 설명해줘."]
)
print(response)
