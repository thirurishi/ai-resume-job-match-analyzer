"""
Resume PDF parsing utilities for the AI Resume & Job Match Analyzer.
"""

import fitz  # PyMuPDF
from core.utils.text_cleaner import clean_text

def extract_text_from_pdf(uploaded_file) -> dict:
    """
    Extract text from a PDF resume file.

    Args:
        uploaded_file: Streamlit uploaded file object (PDF).

    Returns:
        dict: A dictionary containing:
            - raw_text: The cleaned extracted text
            - word_count: Number of words in the cleaned text
            - character_count: Number of characters in the cleaned text
            - page_count: Number of pages in the PDF

    Raises:
        ValueError: If there's an error reading the PDF or extracting text.
    """
    try:
        # Read PDF bytes
        pdf_bytes = uploaded_file.read()

        # Open PDF document
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = len(doc)

        # Extract text from all pages
        text = ""
        for page in doc:
            text += page.get_text()

        # Close document
        doc.close()

        # Clean the extracted text
        cleaned_text = clean_text(text)

        return {
            "raw_text": cleaned_text,
            "word_count": len(cleaned_text.split()) if cleaned_text else 0,
            "character_count": len(cleaned_text),
            "page_count": page_count
        }

    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")