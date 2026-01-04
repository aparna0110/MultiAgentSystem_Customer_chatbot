from agents.tier1_faq_agent import Tier1FAQAgent
from agents.tier2_escalation_agent import Tier2EscalationAgent
from graph.state import AgentState
from agents.manager_agent import ManagerAuditAgent

tier1 = Tier1FAQAgent()
tier2 = Tier2EscalationAgent()
manager = ManagerAuditAgent(confidence_threshold=0.7)

def tier1_node(state: AgentState) -> AgentState:
    print("\n➡️ ENTERED: Tier-1 Agent")
    answer, confidence = tier1.run(state["question"])
    print(f"Tier-1 confidence: {confidence}")
    return {
        "question": state["question"],
        "answer": answer,
        "confidence": confidence,
    }


def tier2_node(state: AgentState) -> AgentState:
    print("\n➡️ ENTERED: Tier-2 Agent")
    answer, confidence = tier2.run(
        question=state["question"],
        tier1_answer=state["answer"]
    )
    print(f"Tier-2 confidence: {confidence}")
    return {
        "question": state["question"],
        "answer": answer,
        "confidence": confidence
    }

def manager_node(state: AgentState) -> AgentState:
    print("\n➡️ ENTERED: Manager/Audit Agent")
    audit = manager.run(
        question=state["question"],
        answer=state["answer"],
        confidence=state["confidence"],
    )
    print(f"Manager status: {audit}")
    return {
        "answer": audit["final_answer"],
        "confidence": audit["confidence"],
        "status": audit["status"],
    }
