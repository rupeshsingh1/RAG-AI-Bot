from fastapi import FastAPI, Request
from application.routes import documents, query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware


# Create FastAPI app
app = FastAPI(
    title="RAG AI Chatbot",
    description="PDF-based Retrieval Augmented Generation using FAISS + GROQ",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev (use specific domain in production)
    allow_credentials=True,
    allow_methods=["*"],  # VERY IMPORTANT
    allow_headers=["*"],  # VERY IMPORTANT
)




# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="application/static"), name="static")

# Configure Jinja2Templates to look in the "templates" directory
templates = Jinja2Templates(directory="application/templates")

# 📄 Document Upload Routes
app.include_router(
    documents.router,
    prefix="/api/v1",
    tags=["Upload Documents"],
)

# 🤖 Query / Chat Routes
app.include_router(
    query.router,
    prefix="/api/v1",
    tags=["Query"],
)

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Context dictionary must include the 'request' object
    context = {"request": request, "message": "Hello from FastAPI!"}
    return templates.TemplateResponse("index.html", context)