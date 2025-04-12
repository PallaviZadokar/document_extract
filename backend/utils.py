import os
import docx
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import fitz  


def extract_text(file_path):

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        print("Extracting text from PDF using PyMuPDF")
        return extract_text_from_pdf(file_path)

    elif ext == ".docx":
        print("Extracting text from Word document")
        return extract_text_from_docx(file_path)

    elif ext in [".jpg", ".jpeg", ".png"]:
        print("Extracting text from image using OCR")
        return extract_text_from_image(file_path)

    else:
        raise ValueError("Unsupported file type")


def extract_text_from_pdf(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print("PyMuPDF failed:", e)
        return ""


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_image(image_path):
    image = Image.open(image_path).convert("RGB")
    return pytesseract.image_to_string(image)


def is_scanned_pdf(pdf_path, threshold=0.1):
    try:
        reader = PdfReader(pdf_path)
        total_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                total_text += page_text.strip()
        average_chars = len(total_text) / max(len(reader.pages), 1)
        return average_chars < (threshold * 100)
    except Exception as e:
        print("Scanned PDF detection failed, assuming scanned:", e)
        return True


def extract_images_from_pdf(pdf_path):
    try:
        pages = convert_from_path(pdf_path, dpi=200)
        return pages
    except Exception as e:
        print("Failed to convert PDF to images:", e)
        return []
