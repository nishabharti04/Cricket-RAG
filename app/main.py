from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import CricketRAG


app = FastAPI(
    title="Cricket LLM RAG API",
    description="A cricket question-answering system using RAG and Llama",
    version="1.0.0"
)

rag = CricketRAG()


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Cricket RAG API is running"
    }


@app.post("/ask")
def ask_question(request: QueryRequest):

    result = rag.ask(request.question)

    return result