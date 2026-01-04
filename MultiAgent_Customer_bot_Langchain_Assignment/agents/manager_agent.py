from llm.azure_llm import get_llm
from langchain_core.prompts import ChatPromptTemplate


class ManagerAuditAgent:
    def __init__(self, confidence_threshold: float = 0.6):
        self.confidence_threshold = confidence_threshold
        self.llm = get_llm(temperature=0)

        self.prompt = ChatPromptTemplate.from_template(open("prompts/manager.txt").read()       
        )

        self.chain = self.prompt | self.llm

    def run(self, question: str, answer: str, confidence: float) -> dict:
        # Hard rule first (no LLM cost)
        if confidence < self.confidence_threshold:
            return {
                "final_answer": answer,
                "confidence": confidence,
                "status": "needs_review",
                "reason": "Confidence below threshold"
            }

        # Soft quality check via LLM
        result = self.chain.invoke(
            {
                "question": question,
                "answer": answer,
                "confidence": confidence
            }
        )

        decision = result.content.lower()

        if "needs_review" in decision:
            return {
                "final_answer": answer,
                "confidence": confidence,
                "status": "needs_review",
                "reason": "Audit agent flagged the response"
            }

        return {
            "final_answer": answer,
            "confidence": confidence,
            "status": "approved",
            "reason": "Response approved by audit agent"
        }
