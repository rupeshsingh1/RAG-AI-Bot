from fastapi import APIRouter, HTTPException
from application.services.retrieval_service import search_similar_chunks
from application.services.chat_service import generate_answer
from pydantic import BaseModel
from application.core.logger import logger

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(data: QuestionRequest):
    try:
        logger.info(f"Question received: {data.question}")

        # 🔍 Retrieve context
        chunks = search_similar_chunks(data.question)

        if not chunks:
            return {"answer": "No relevant information found"}

        # 🤖 Generate answer
        answer = generate_answer(chunks, data.question)

        return {
            "question": data.question,
            "answer": answer,
            "context_used": chunks
        }

    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")