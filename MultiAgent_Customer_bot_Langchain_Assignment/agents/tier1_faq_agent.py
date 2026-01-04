from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from operator import itemgetter

from llm.azure_llm import get_llm
from knowledge.vector_store import load_faq_vector_store


class Tier1FAQAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0)
        self.vector_store = load_faq_vector_store()

        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        self.prompt = ChatPromptTemplate.from_template(
            open("prompts/tier1.txt").read()
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.chain = (
            {
                "context": itemgetter("question") | self.retriever | RunnableLambda(format_docs),
                "question": itemgetter("question"),
            }
            | self.prompt
            | self.llm
        )

    def run(self, query: str) -> str:
        if not isinstance(query, str):
            raise ValueError("Query must be a string")
        
        # 1️⃣ Retrieve docs explicitly
        #docs = self.retriever.invoke(query)
        docs_with_scores = self.vector_store.similarity_search_with_score(
            query,
            k=3
        )
        documents = [doc for doc, _ in docs_with_scores]
        scores = [score for _, score in docs_with_scores]

        # 2️⃣ Invoke LLM chain
        response = self.chain.invoke({"question": query})

        answer = response.content
        #confidence = self._calculate_confidence(answer, docs)
        confidence = self._calculate_confidence(answer, scores)

        print("Answer:", answer)
        print("Confidence:", confidence)

        return answer, confidence
        
    def _calculate_confidence(self, answer: str, scores: list[float], max_distance: float = 2.0) -> float:
        """
        Compute a confidence score based on:
        1. LLM uncertainty in the answer
        2. Retriever similarity scores (distance or cosine)

        Args:
            answer (str): LLM-generated answer text
            scores (list[float]): List of similarity/distance scores from vector store
            max_distance (float): Maximum expected L2 distance (for scaling)

        Returns:
            float: Confidence score between 0.0 and 1.0
        """

        # 1️⃣ Penalize uncertain language
        if any(phrase in answer.lower() for phrase in ["not sure", "don't know", "uncertain"]):
            return 0.3

        # 2️⃣ If no retrieved documents, very low confidence
        if not scores:
            return 0.2

        # 3️⃣ Compute average score
        avg_score = sum(scores) / len(scores)

        # 4️⃣ Map FAISS L2 distance to 0–1 confidence (smaller distance = higher confidence)
        confidence = max(0.0, min(1.0, 1 - avg_score / max_distance))

        return confidence

    
# if __name__ == "__main__":
#     agent = Tier1FAQAgent()
#     query = "How can I reset my password?"
#     answer, confidence = agent.run(query)
#     print(f"Answer: {answer}\nConfidence: {confidence}")