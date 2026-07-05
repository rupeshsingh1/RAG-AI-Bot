from .retriever import Retriever
from .gemini_service import GeminiService

class RAGPipeline:

    def __init__(self, vector_store):

        self.retriever = Retriever(vector_store)
        self.llm = GeminiService()

    def generate_answer(self, question):

        docs = self.retriever.retrieve(question)

        context = "\n".join(docs)

        prompt = f"""
        Use the context below to answer the question.

        Context:
        {context}

        Question:
        {question}
        """

        return self.llm.generate(prompt)