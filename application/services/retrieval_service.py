import faiss
import numpy as np
import json
import os

from application.core.logger import logger
from application.services.embedding_service import generate_embeddings

INDEX_PATH = "vector/faiss_index.index"
METADATA_PATH = "vector/metadata.json"


def search_similar_chunks(query, top_k=5):
    try:
        logger.info("Searching similar chunks")

        if not os.path.exists(INDEX_PATH) or not os.path.exists(METADATA_PATH):
            raise ValueError("FAISS index or metadata not found")

        # Load FAISS index
        index = faiss.read_index(INDEX_PATH)

        # Load metadata
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # Generate embedding for query
        query_embedding = generate_embeddings([query])[0]
        query_embedding = np.array([query_embedding]).astype("float32")

        # Search
        distances, indices = index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(metadata):
                results.append(metadata[idx])

        return results

    except Exception as e:
        logger.error(f"Retrieval error: {str(e)}")
        raise