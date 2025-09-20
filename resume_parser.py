
"""resume_parser.py
Helpers to extract text from PDF/DOCX/TXT resumes.
Uses PyMuPDF for PDFs and python-docx for docx. For MVP, we support plain TXT too.
"""
import os

def extract_text_from_txt(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def extract_text_from_pdf(path: str) -> str:
    try:
        import fitz  # PyMuPDF
    except Exception as e:
        raise ImportError('PyMuPDF (fitz) is required to extract from PDF. Install via pip install pymupdf') from e
    doc = fitz.open(path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(path: str) -> str:
    try:
        import docx2txt
    except Exception as e:
        raise ImportError('docx2txt/python-docx required to extract from DOCX. Install via pip install docx2txt') from e
    text = docx2txt.process(path)
    return text

def extract_resume_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.txt':
        return extract_text_from_txt(path)
    elif ext == '.pdf':
        return extract_text_from_pdf(path)
    elif ext in ('.docx', '.doc'):
        return extract_text_from_docx(path)
    else:
        raise ValueError('Unsupported resume format: ' + ext)
