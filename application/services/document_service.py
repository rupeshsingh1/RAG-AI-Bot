import os
from fastapi import UploadFile
from application.utils.file_utils import create_upload_folder, generate_unique_filename
from pypdf import PdfReader

UPLOAD_FOLDER = "app/uploads/pdfs"


async def save_pdf(file: UploadFile) -> str:
    create_upload_folder(UPLOAD_FOLDER)

    filename = generate_unique_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return file_path


def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def chunk_text(text: str, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks