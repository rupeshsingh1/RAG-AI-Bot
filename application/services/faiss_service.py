import faiss
import numpy as np
import os
import json

from application.core.logger import logger

INDEX_PATH = "vector/faiss_index.index"
METADATA_PATH = "vector/metadata.json"


def store_embeddings(embeddings, chunks):
    try:
        logger.info("Storing embeddings in FAISS")

        # Ensure directory exists
        os.makedirs("vector", exist_ok=True)

        # Convert to float32 (MANDATORY for FAISS)
        embeddings = np.array(embeddings).astype("float32")
        dimension = embeddings.shape[1]

        # Load or create index
        if os.path.exists(INDEX_PATH):
            logger.info("Loading existing FAISS index")
            index = faiss.read_index(INDEX_PATH)
        else:
            logger.info("Creating new FAISS index")
            index = faiss.IndexFlatL2(dimension)

        # Add embeddings
        index.add(embeddings)

        # Save FAISS index
        faiss.write_index(index, INDEX_PATH)

        # ✅ STORE METADATA (VERY IMPORTANT)
        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        else:
            metadata = []

        metadata.extend(chunks)

        with open(METADATA_PATH, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        logger.info(f"Stored {len(embeddings)} embeddings + metadata")

        return True

    except Exception as e:
        logger.error(f"FAISS storage error: {str(e)}")
        raise