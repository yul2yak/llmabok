import requests
from langchain_huggingface import HuggingFacePipeline
from huggingface_hub import login, hf_hub_download
import os
import dotenv
dotenv.load_dotenv()


# r = requests.get("https://huggingface.co")
# print(r.status_code)

print(os.getenv("HUGGINGFACEHUB_API_TOKEN"))
login(token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

# 먼저 파일 직접 다운로드 시도 (테스트)
# config_path = hf_hub_download("google/gemma-3-1b-it", "config.json")
# print("다운로드 성공:", config_path)

llm = HuggingFacePipeline.from_model_id(
    model_id="google/gemma-3-1b-it",
    task="text-generation",
)

response = llm.invoke("너는 이름이 뭐야? Gemini 랑 무슨 차이가 있어?")
print(response)
