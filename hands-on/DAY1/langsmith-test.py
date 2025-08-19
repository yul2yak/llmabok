# Create a LANGSMITH_API_KEY in Settings > API Keys
from langsmith import Client
client = Client(api_key='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')
prompt = client.pull_prompt("hardkothari/prompt-maker", include_model=True)

result = prompt.invoke("2025년 8월 한국의 대통령은 누구인가요?")
print(result)
