# from graph.workflow import build_graph

# graph = build_graph()

# query = {"question": "How can I reset my password?"}

# result = graph.invoke(query)

# print("\nFinal Output:")
# print(result)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from graph.workflow import build_graph

support_graph = build_graph()

app = FastAPI(
    title="Multi-Agent Customer Support Bot",
    version="1.0.0"
)


# -------- Request / Response Schemas --------

class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    confidence: float
    status: str


# -------- Health Check --------

@app.get("/health")
def health_check():
    return {"status": "ok"}


# -------- Chat Endpoint --------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        result = support_graph.invoke(
            {"question": request.question}
        )

        return {
            "answer": result["answer"],
            "confidence": result["confidence"],
            "status": result.get("status", "approved"),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))