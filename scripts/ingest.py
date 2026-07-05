from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore

docs = [
    "FastAPI is a modern Python web framework.",
    "FAISS is a library for efficient similarity search.",
    "RAG stands for Retrieval Augmented Generation."
]

embedding_service = EmbeddingService()

embeddings = embedding_service.embed(docs)

vector_store = VectorStore(dim=len(embeddings[0]))

vector_store.add(embeddings, docs)

print("Documents indexed")