from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field, ValidationError
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.exceptions import OutputParserException
import re
from typing import Any
import json
import dotenv
dotenv.load_dotenv()


class RobustPydanticOutputParser(PydanticOutputParser):
    """
    LLM 출력 또는 Python 객체를 Pydantic 모델로 안전하게 변환하는 파서.
    - 문자열: 후처리(clean ```json) 후 parse
    - list/dict: 바로 Pydantic 객체로 변환
    - JSON 형식 강제 검사 및 ValidationError 처리
    """

    def parse(self, obj: Any):
        # 이미 list/dict이면 바로 Pydantic 객체 생성
        if isinstance(obj, (list, dict)):
            try:
                return self.pydantic_object.parse_obj(obj)
            except ValidationError as e:
                raise OutputParserException(
                    f"Validation failed on Python object: {e}\nInput: {obj}")

        # 문자열이면 후처리
        if isinstance(obj, str):
            # ```json 제거 및 공백 strip
            cleaned = re.sub(r"```json|```", "", obj).strip()
            # JSON 형식인지 강제 검사
            try:
                data = json.loads(cleaned)
            except json.JSONDecodeError as e:
                raise OutputParserException(
                    f"Invalid JSON format after cleaning: {e}\nCleaned text: {cleaned}")

            # Pydantic 객체 생성
            try:
                return self.pydantic_object.parse_obj(data)
            except ValidationError as e:
                raise OutputParserException(
                    f"Pydantic validation failed: {e}\nData: {data}")

        raise OutputParserException(f"Unsupported input type: {type(obj)}")


with open('data/AI 에이전트 동향_short.txt', 'r', encoding='utf-8') as f:
    file = f.read()

prompt = PromptTemplate.from_template('''
다음의 context 를 읽고, 의미있는 단위로 쪼개서 반드시 format 예제와 같은 형식으로 답해주세요. 

context: {context}
format: 
[
    {{"title": "제목", "content": "내용"}},
    ...
]

모든 content는 반드시 내용이 있어야 하며, null이 되면 안됩니다.
절대로 ```json 같은 코드 블록을 사용하지 마세요.  
오직 [ ... ] JSON 배열 형식으로만 답하세요.  
다른 텍스트, 설명, 마크다운은 금지입니다.
''')


class MeaningfulChunk(BaseModel):
    title: str = Field(description="제목")
    content: str = Field(description="내용")


class MeaningfulChunkList(BaseModel):
    chunks: list[MeaningfulChunk] = Field(description="의미있는 단위로 쪼개진 콘텐츠 목록")


output_parser = RobustPydanticOutputParser(pydantic_object=MeaningfulChunkList)

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

# print(file)
chain = {
    'context': lambda x: file,
    # 'format': lambda x: output_parser.get_format_instructions()
} | prompt | llm  # | output_parser
response = chain.invoke({})

output_parser.parse(response.content)
