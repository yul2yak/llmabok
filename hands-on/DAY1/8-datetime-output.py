from langchain.output_parsers import DatetimeOutputParser
import dotenv
dotenv.load_dotenv()

output_parser = DatetimeOutputParser()

print(output_parser)
