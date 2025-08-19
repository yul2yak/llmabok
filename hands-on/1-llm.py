from langchain.chat_models import init_chat_model
import dotenv
dotenv.load_dotenv()


def main():
    llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

    question = input("질문을 입력하세요: ")
    response = llm.invoke(question)
    print(response)


if __name__ == "__main__":
    main()
