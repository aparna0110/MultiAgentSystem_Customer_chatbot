from langchain_core.prompts import ChatPromptTemplate
from llm.azure_llm import get_llm


class Tier2EscalationAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.2)

        self.prompt = ChatPromptTemplate.from_template(
            open("prompts/tier2.txt").read()
        )

    def run(self, question: str, tier1_answer: str | None=None) -> str:
        response = self.llm.invoke(
            self.prompt.format_messages(
                question=question,
                tier1_answer=tier1_answer or "N/A",
            )
        )
        
        answer = response.content

        # Tier-2 is authoritative
        confidence = 0.9

        return answer, confidence
    
# if __name__ == "__main__":
#     agent = Tier2EscalationAgent()

#     question = "How can I reset my password?"
#     tier1_answer = "You can reset your password using the Forgot Password option."
#     confidence = 0.45

#     result = agent.run(
#         question=question,
#         tier1_answer=tier1_answer,
#         confidence=confidence
#     )

#     print("Tier-2 Answer:")
#     print(result)