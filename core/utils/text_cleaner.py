"""
Text cleaning utilities for the AI Resume & Job Match Analyzer.
"""

def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing excessive spaces,
    repeated blank lines, and normalizing line breaks.

    Args:
        text (str): The raw text to clean.

    Returns:
        str: The cleaned text.
    """
    if not text:
        return ""

    # Normalize line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove excessive spaces (multiple spaces to single)
    import re
    text = re.sub(r' +', ' ', text)

    # Remove repeated blank lines (more than one consecutive newline)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text