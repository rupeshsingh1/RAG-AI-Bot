import os
from uuid import uuid4

def create_upload_folder(path: str):
    os.makedirs(path, exist_ok=True)


def generate_unique_filename(filename: str):
    return f"{uuid4()}_{filename}"


def validate_pdf(content_type: str):
    return content_type == "application/pdf"