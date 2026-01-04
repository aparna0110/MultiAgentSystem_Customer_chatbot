from typing import TypedDict, Optional

class AgentState(TypedDict):
    question: str
    answer: Optional[str]   
    confidence: Optional[float]
    