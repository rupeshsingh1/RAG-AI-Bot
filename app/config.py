import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

FAISS_INDEX_PATH = "vector_store/faiss_index"