from sentence_transformers import SentenceTransformer
from application.core.logger import logger

# ✅ Load model once (important for performance)
# 
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    try:
        logger.info(f"Generating embeddings for {len(chunks)} chunks")

        # ✅ Batch embedding (FAST)
        embeddings = model.encode(
            chunks,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        return embeddings.tolist()  # convert to list for FAISS

    except Exception as e:
        logger.error(f"Embedding error: {str(e)}")
        raise