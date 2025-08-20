Retrievers는 LangChain에서 자연어 쿼리를 입력받아 관련 문서 목록을 반환하는 인터페이스입니다. 주요 특징과 개념은 다음과 같습니다:

기본 개념: Retriever는 벡터 스토어(vector store)보다 더 일반적인 개념으로, 문서를 저장할 필요 없이 쿼리에 맞는 문서를 반환하는 역할을 합니다. 예를 들어, Wikipedia 검색이나 Amazon Kendra 같은 검색 API도 Retriever로 구현할 수 있습니다[3][4].

입력과 출력: Retriever는 문자열 쿼리를 입력으로 받고, LangChain의 표준 Document 객체 리스트를 출력합니다. Document 객체는 page_content(문서 내용)와 metadata(문서 관련 메타데이터)를 포함합니다[4].

인터페이스: LangChain의 Retriever 클래스는 _get_relevant_documents(query: str) 메서드를 구현해야 하며, 이 메서드는 쿼리에 가장 관련성 높은 문서 리스트를 반환합니다. Retriever는 Runnable 인터페이스를 구현하여 invoke 메서드로 쿼리를 전달할 수 있습니다[4].

종류: Retriever는 다양한 유형이 있습니다.

벡터 스토어 기반 Retriever
검색 API 기반 Retriever (예: Wikipedia, Amazon Kendra)
관계형 데이터베이스나 그래프 데이터베이스 기반 Retriever (텍스트-투-SQL 변환 등을 활용)
자체 문서 코퍼스를 인덱싱하여 검색하는 Retriever 등[3][4].
활용: Retriever는 RAG(Retrieval Augmented Generation) 같은 AI 애플리케이션에서 중요한 역할을 하며, LangChain에서는 Retriever를 체인(chains) 내에서 쉽게 조합하여 사용할 수 있습니다[1][2].

요약하면, Retriever는 자연어 쿼리를 받아 관련 문서를 찾아주는 범용 인터페이스로, 다양한 데이터 소스와 검색 방식을 추상화하여 일관된 방식으로 문서 검색 기능을 제공합니다[3][4].