# utils/file_parser.py
import io
from PyPDF2 import PdfReader
from docx import Document
import streamlit as st # For st.error

def extract_text_from_pdf(file_bytes_io: io.BytesIO) -> str:
    """Extracts text from a PDF file."""
    text = ""
    try:
        reader = PdfReader(file_bytes_io)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        print(f"Error reading PDF: {e}") # For console debugging
    return text

def extract_text_from_docx(file_bytes_io: io.BytesIO) -> str:
    """Extracts text from a DOCX file."""
    text = ""
    try:
        document = Document(file_bytes_io)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
        print(f"Error reading DOCX: {e}") # For console debugging
    return text

# Note: For .txt files, Streamlit's file_uploader.read().decode('utf-8') is often sufficient
# and can be handled directly in app.py or a simple wrapper function here.
# For now, it's handled in app.py directly for simplicity.
