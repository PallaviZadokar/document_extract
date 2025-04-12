from fastapi import FastAPI, File, UploadFile
from backend.utils import extract_text, is_scanned_pdf, extract_images_from_pdf
from backend.extract import extract_fields_from_text
from backend.classify import classify_document_type
from models.donut_model import extract_using_donut
import os

app = FastAPI()

@app.post("/extract")
async def extract_fields(file: UploadFile = File(...)):
    content = await file.read()
    ext = os.path.splitext(file.filename)[1].lower()
    file_path = f"temp{ext}"

    
    with open(file_path, "wb") as f:
        f.write(content)

    
    if ext in [".jpg", ".jpeg", ".png"]:
        print("Image detected — using Donut model")
        donut_output = extract_using_donut(file_path)
        extracted_text = donut_output

    elif ext == ".pdf":
        if is_scanned_pdf(file_path):
            print("Scanned PDF detected — converting to images")
            pages = extract_images_from_pdf(file_path)
            donut_output = ""
            for i, page in enumerate(pages):
                temp_img_path = f"temp_page_{i}.png"
                page.save(temp_img_path)
                donut_output += extract_using_donut(temp_img_path) + "\n"
            extracted_text = donut_output
        else:
            print("Text-based PDF — using text extractor")
            extracted_text = extract_text(file_path)

    elif ext == ".docx":
        print("Word document — using text extractor")
        extracted_text = extract_text(file_path)

    else:
        raise ValueError("Unsupported file type")

    
    doc_type = classify_document_type(extracted_text)
    data = extract_fields_from_text(extracted_text)

    return {
        "file": file.filename,
        "document_type": doc_type,
        "extracted_data": data
    }
