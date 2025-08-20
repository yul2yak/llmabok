from langchain.schema.runnable import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
import dotenv
dotenv.load_dotenv()


class SimpleRetriever(BaseRetriever):
    docs: list[Document]
    k: int = 5

    def _get_relevant_documents(self, query: str) -> list[Document]:
        return self.docs[:self.k]


document = Document(
    page_content='2025년 6월 3일에 당선된 제 21대 대통령은 더불어민주당 이재명이다.',
    metadata={'source': 'https://example.com'}
)

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# response = llm.invoke('한국의 대통령은?')
# print(response.content)

prompt = PromptTemplate.from_template("""
다음의 context를 읽고, 질문에 답해줘.
context: {context}
질문: {question}
""")

chain = prompt | llm

retriever = SimpleRetriever(docs=[document], k=1)
context = retriever.invoke('한국의 대통령은?')
# print(context)

response = chain.invoke({
    'question': '한국의 대통령은?',
    'context': retriever.invoke('한국의 대통령은?')
})
# print(response.content)

chain = {
    'context': retriever,
    'question': RunnablePassthrough()
} | prompt | llm
response = chain.invoke('한국의 대통령은?')
print(response.content)
