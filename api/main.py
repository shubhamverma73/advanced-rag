from fastapi import FastAPI
from pydantic import BaseModel
from chat_api import chat

app = FastAPI(
    title="Advanced RAG API",
    description="Production Ready Advanced RAG",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    query: str
    answer: str


@app.get("/")
def home():
    return {
        "message": "Advanced RAG API is Running 🚀"
    }


@app.post("/chat", response_model=ChatResponse)
def ask_question(request: ChatRequest):

    answer = chat(request.query)

    return {
        "query": request.query,
        "answer": answer
    }