"""
Job description parsing utilities for the AI Resume & Job Match Analyzer.
"""

from core.utils.text_cleaner import clean_text

def parse_job_description(job_text: str) -> dict:
    """
    Parse and clean a job description text.

    Args:
        job_text (str): The raw job description text.

    Returns:
        dict: A dictionary containing:
            - raw_text: The cleaned job description text
            - word_count: Number of words in the cleaned text
            - character_count: Number of characters in the cleaned text
    """
    cleaned_text = clean_text(job_text)

    return {
        "raw_text": cleaned_text,
        "word_count": len(cleaned_text.split()) if cleaned_text else 0,
        "character_count": len(cleaned_text)
    }