from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.services.rag_pipeline import RAGPipeline
from app.services.vector_store import VectorStore

router = APIRouter()

vector_store = VectorStore(dim=384)
rag = RAGPipeline(vector_store)

@router.post("/chat")

def chat(request: ChatRequest):

    answer = rag.generate_answer(request.question)

    return {"answer": answer}