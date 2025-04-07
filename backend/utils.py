import os
import docx
import pdfplumber
import pytesseract
from pdf2image import convert_from_path


try:
    from models.donut_model import extract_using_donut
    USE_DONUT = True
except ImportError:
    USE_DONUT = False

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        print(f"pdfplumber failed: {e}")
        return None

def extract_text_via_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def donut_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    results = [extract_using_donut(img) for img in images]
    return "\n".join(results)

def fallback_donut(file_path):
    if not USE_DONUT:
        return "Donut model not available"
    try:
        if file_path.lower().endswith(".pdf"):
            return donut_from_pdf(file_path)
        else:
            return extract_using_donut(file_path)
    except Exception as e:
        return f"Error using Donut model: {str(e)}"

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".pdf":
        text = extract_text_from_pdf(file_path)
        if text and text.strip():
            return text
        else:
            try:
                return extract_text_via_ocr(file_path)
            except Exception as e:
                print(f"OCR fallback failed: {e}")
                if USE_DONUT:
                    return fallback_donut(file_path)
                else:
                    raise RuntimeError("Text extraction failed and OCR fallback unavailable.")
    else:
        raise ValueError("Unsupported file type")
