import os
import requests
import tempfile
import trafilatura
import fitz  # PyMuPDF
from docx import Document
from config import settings

def extract_text(source: str) -> str:
    if not source:
        return ""

    #local file(for using with streamlit)
    if os.path.exists(source):
        ext = os.path.splitext(source)[1].lower()
        if ext == ".pdf":
            return extract_text_from_pdf(source)
        elif ext == ".docx":
            return extract_text_from_docx(source)
        elif ext == ".txt":
            with open(source, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        else:
            return ""
    
    #url
    try:
        response = requests.get(source, timeout=settings.EXTERNAL_REQUEST_TIMEOUT)
        if response.status_code != 200:
            return ""
        
        content_type = response.headers.get("content-type", "").lower()
        
        # PDF over HTTP
        if "application/pdf" in content_type or source.lower().endswith(".pdf"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(response.content)
                tmp_path = tmp.name
            text = extract_text_from_pdf(tmp_path)
            os.remove(tmp_path)
            return text
        
        # DOCX over HTTP
        if "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in content_type or source.lower().endswith(".docx"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(response.content)
                tmp_path = tmp.name
            text = extract_text_from_docx(tmp_path)
            os.remove(tmp_path)
            return text
        
        # HTML pages (blogs, Springer, etc.)
        if "text/html" in content_type:
            downloaded = trafilatura.fetch_url(source)
            if downloaded:
                return trafilatura.extract(downloaded) or ""
            else:
                return ""
        
        return ""
    except Exception as e:
        print(f"[extract_text] Error: {e}")
        return ""

def extract_text_from_pdf(path: str) -> str:
    """extract text from pdf"""
    text = ""
    try:
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"[PDF extraction error] {e}")
    return text

def extract_text_from_docx(path: str) -> str:
    """extract text from docx"""
    text = ""
    try:
        doc = Document(path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"[DOCX extraction error] {e}")
    return text
