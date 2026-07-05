from .embedding_service import EmbeddingService
from .vector_store import VectorStore

class Retriever:

    def __init__(self, vector_store):
        self.embedding_service = EmbeddingService()
        self.vector_store = vector_store

    def retrieve(self, query):

        query_embedding = self.embedding_service.embed([query])

        docs = self.vector_store.search(query_embedding)

        return docs