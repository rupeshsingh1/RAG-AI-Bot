import faiss
import numpy as np
import pickle

class VectorStore:

    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []

    def add(self, embeddings, docs):

        self.index.add(np.array(embeddings))
        self.documents.extend(docs)

    def search(self, query_embedding, k=3):

        distances, indices = self.index.search(query_embedding, k)

        results = []
        for idx in indices[0]:
            results.append(self.documents[idx])

        return results