import docx
import fitz
import trafilatura
import os

def extract_text_from_pdf(file_path):
    text = " "
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    
def extract_text_from_url(url):
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        return trafilatura.extract(downloaded)
    return trafilatura.extract(downloaded)    

def extract_text(file_path_or_url):
    if file_path_or_url.startswith("http"):
        return extract_text_from_url(file_path_or_url)
    
    ext = os.path.splitext(file_path_or_url)[-1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path_or_url)
    elif ext == ".docx":
        return extract_text_from_docx(file_path_or_url)
    elif ext == ".txt":
        return extract_text_from_txt(file_path_or_url)
    else:
        raise ValueError("Unsupported file format or invalid URL.")