from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import EnumOutputParser
from enum import Enum
import dotenv
dotenv.load_dotenv()


class Color(Enum):
    RED = "빨강"
    BLUE = "파랑"
    YELLOW = "노랑"


output_parser = EnumOutputParser(enum=Color)
print(output_parser.get_format_instructions())

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
prompt = PromptTemplate.from_template("{object}의 색깔은? 출력은 {format}")
prompt = prompt.partial(format=output_parser.get_format_instructions())
prompt.pretty_print()
chain = prompt | llm | output_parser
response = chain.invoke({"object": "사과"})
print(response)
