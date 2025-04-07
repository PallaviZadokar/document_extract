from fastapi import FastAPI, File, UploadFile
from backend.utils import extract_text
from backend.extract import extract_fields_from_text
from backend.classify import classify_document_type
import os

app = FastAPI()

@app.post("/extract")
async def extract_fields(file: UploadFile = File(...)):
    content = await file.read()
    file_path = f"temp{os.path.splitext(file.filename)[1]}"

    with open(file_path, "wb") as f:
        f.write(content)

    text = extract_text(file_path)
    doc_type = classify_document_type(text)
    data = extract_fields_from_text(text)

    return {
        "file": file.filename,
        "document_type": doc_type,
        "extracted_data": data
    }

