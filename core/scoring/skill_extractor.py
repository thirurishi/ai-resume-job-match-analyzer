"""
Skill extraction utilities for the AI Resume & Job Match Analyzer.
"""

import re

# Predefined professional skill dictionary
SKILLS_DICTIONARY = [
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Tableau",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "FastAPI",
    "Streamlit",
    "Docker",
    "Git",
    "GitHub",
    "PostgreSQL",
    "MySQL",
    "SQLite",
    "MongoDB",
    "AWS",
    "Azure",
    "GCP",
    "Airflow",
    "ETL",
    "Data Cleaning",
    "Data Visualization",
    "Statistics",
    "A/B Testing",
    "KPI",
    "Dashboarding",
    "Reporting",
    "Business Intelligence",
    "Data Analysis",
    "Data Science",
    "API",
    "REST API",
    "Linux"
]

# Skill aliases for normalization
SKILL_ALIASES = {
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "ms excel": "Excel",
    "microsoft excel": "Excel",
    "sklearn": "Scikit-learn",
    "postgres": "PostgreSQL",
    "rest": "REST API",
    "restful": "REST API",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "nlp": "NLP",
    "ml": "Machine Learning",
    "ai": "Machine Learning",
    "artificial intelligence": "Machine Learning",
    "bi": "Business Intelligence",
    "etl": "ETL"
}


def extract_skills(text: str) -> list:
    """
    Extract skills from text using predefined skill dictionary.
    
    Args:
        text (str): The text to extract skills from.
    
    Returns:
        list: A sorted list of unique skills found in the text.
    """
    if not text:
        return []
    
    # Convert text to lowercase for matching
    text_lower = text.lower()
    
    found_skills = set()
    
    # Check for aliases first
    for alias, skill in SKILL_ALIASES.items():
        pattern = r'\b' + re.escape(alias) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
    
    # Check for skills in dictionary
    for skill in SKILLS_DICTIONARY:
        skill_lower = skill.lower()
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
    
    # Return sorted list
    return sorted(list(found_skills))