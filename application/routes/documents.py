from fastapi import APIRouter, UploadFile, File, HTTPException
from application.services.document_service import (
    save_pdf,
    extract_text_from_pdf,
    chunk_text
)
from application.services.embedding_service import generate_embeddings
from application.services.faiss_service import store_embeddings
from application.core.logger import logger

router = APIRouter()


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    logger.info("Upload PDF endpoint called")

    if not file.filename.endswith(".pdf"):
        logger.info(f"Uploaded file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    try:
        # ✅ Save PDF
        file_path = await save_pdf(file)
        logger.info(f"File saved at {file_path}")

        # ✅ Extract text
        text = extract_text_from_pdf(file_path)

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")

        logger.info("Text extracted from PDF")

        # ✅ Chunk text
        chunks = chunk_text(text)
        logger.info(f"Created {len(chunks)} chunks")

        # ✅ Generate embeddings (MiniLM)
        try:
            embeddings = generate_embeddings(chunks)
        except Exception as e:
            logger.error(f"Embedding failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Embedding Error: {str(e)}")

        logger.info("Embeddings generated successfully")

        # ✅ Store in FAISS
        store_embeddings(embeddings, chunks)
        logger.info("Embeddings stored in FAISS")

        return {
            "message": "PDF processed successfully",
            "file_path": file_path,
            "num_chunks": len(chunks),
            "embedding_dim": len(embeddings[0]) if embeddings else 0
        }

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")