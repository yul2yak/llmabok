import dotenv
dotenv.load_dotenv()

from langchain.chat_models import init_chat_model
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

response = llm.invoke("한국의 수도는?")
print(response)
