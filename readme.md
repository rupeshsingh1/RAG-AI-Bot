# 🤖 RAG AI Chatbot

A simple Retrieval-Augmented Generation (RAG) chatbot using FastAPI, FAISS, Sentence Transformers, and Grok API.

---

## 🚀 Features

* Upload PDFs
* Store embeddings in FAISS
* Ask questions from documents
* Get AI-generated answers

---

## 🛠 Tech Stack

* FastAPI
* FAISS
* Sentence Transformers (MiniLM)
* Grok API

---

## 📁 Structure

```
app/
 ├── main.py
 ├── routes/
 ├── services/
 ├── templates/

data/
 ├── uploads/
 ├── faiss_index/
```

---

## ⚙️ Setup

```bash
git clone <repo-url>
cd rag-ai-chatbot
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

Create `.env`:

```
GROK_API_KEY=your_key
```

---

## ▶️ Run

```bash
uvicorn app.main:app --reload
```

---

## 📡 API

**Upload PDF**

```
POST /upload
```

**Chat**

```
POST /chat
```

---

## 🔄 Flow

Query → Embedding → FAISS → Context → Grok → Answer

---

## 👨‍💻 Author

Rupesh Singh
