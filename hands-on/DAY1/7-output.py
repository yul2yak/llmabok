from enum import Enum
from langchain.output_parsers import DatetimeOutputParser, EnumOutputParser
import json
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
import dotenv
dotenv.load_dotenv()

prompt = PromptTemplate.from_template("""
{country}의 수도는? 다음 JSON 형식으로 응답하세요. 
출력 예시:
{{"country": "한국", "capital": "서울"}}
""")

llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
chain = prompt | llm

response = chain.invoke("중국")
print(response.content)


class User(BaseModel):
    name: str = Field(description="사용자의 이름")
    age: int = Field(description="사용자의 나이", gt=0)


hong = User(name="홍길동", age="30")
lee = User(name="이순신", age=45)


class Capital(BaseModel):
    country: str = Field(description="국가")
    capital: str = Field(description="수도")


output_parser = PydanticOutputParser(pydantic_object=Capital)

# print(output_parser.get_format_instructions())

# response = output_parser.parse(response.content)
# print(response)

prompt = PromptTemplate.from_template("""
{country}의 수도는? 다음 형식으로 응답하세요.
{format}
""")
prompt = prompt.partial(format=output_parser.get_format_instructions())
prompt.pretty_print()

chain = prompt | llm | output_parser
response = chain.invoke({"country": "한국"})
print(response)

output_parser = JsonOutputParser(pydantic_object=Capital)
chain = prompt | llm | output_parser
response = chain.invoke({"country": "한국"})
print(response)

print(json.dumps(response, ensure_ascii=False, indent=2))

output_parser = DatetimeOutputParser()
print(output_parser.get_format_instructions())

prompt = PromptTemplate.from_template("""
{company}의 창립기념일은? 다음 형식으로 답변해 주세요. 
{format}""")
prompt = prompt.partial(format=output_parser.get_format_instructions())
chain = prompt | llm | output_parser
response = chain.invoke({"company": "삼성전자"})
print(response.strftime("삼성전자 창립기념일은 %Y년 %m월 %d일"))


class Color(Enum):
    RED = "빨강"
    GREEN = "초록"
    BLUE = "파랑"


output_parser = EnumOutputParser(enum=Color)
print(output_parser.get_format_instructions())
prompt = PromptTemplate.from_template("""
보라색은 어떤 색에 가깝지?
{format}
""")
prompt = prompt.partial(format=output_parser.get_format_instructions())
chain = prompt | llm | output_parser
response = chain.invoke({})
print(response)
