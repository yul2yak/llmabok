from langchain import hub
from langchain_core.prompts import load_prompt
from langchain_core.prompts import PromptTemplate
import dotenv
dotenv.load_dotenv()


# prompt = PromptTemplate.from_template("{country}의 수도는?")
# prompt.save("capital.json")
# prompt.save("capital.yaml")

# prompt = load_prompt("capital.json")
# print(prompt)
# prompt = load_prompt("capital.yaml")
# print(prompt)

# prompt = hub.pull('rlm/rag-prompt')
prompt = hub.pull('hardkothari/prompt-maker')
prompt_val = prompt.invoke(
    {'task': '회사의 root 인증서를 찾는 방법은?', 'lazy_prompt': ''})
print(prompt_val)

# prompt_owner = 'yul2ya'
# prompt_title = 'rag-prompt'
# hub.push(f'{prompt_title}', prompt)
