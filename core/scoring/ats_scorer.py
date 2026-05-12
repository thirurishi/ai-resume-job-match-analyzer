"""
ATS scoring engine combining skill match, semantic similarity, and completeness.
"""

import re
from core.scoring.match_engine import analyze_skill_match
from core.scoring.semantic_matcher import calculate_semantic_similarity


def calculate_completeness_score(resume_text: str) -> float:
    """
    Calculate resume completeness score based on presence of key sections.
    
    Args:
        resume_text (str): The resume text.
    
    Returns:
        float: Completeness score as percentage (0-100).
    """
    sections = ["education", "experience", "projects", "skills", "certifications"]
    found_sections = 0
    
    text_lower = resume_text.lower()
    
    for section in sections:
        # Search for section keywords with word boundaries
        pattern = r'\b' + section + r'\b'
        if re.search(pattern, text_lower):
            found_sections += 1
    
    # Each section is worth 20% (5 sections total)
    completeness_percentage = (found_sections / len(sections)) * 100
    
    return round(completeness_percentage, 2)


def calculate_ats_score(resume_text: str, job_text: str) -> dict:
    """
    Calculate comprehensive ATS score using skill match, semantic similarity,
    and resume completeness.
    
    Scoring weights:
    - Skill Match: 50%
    - Semantic Similarity: 30%
    - Resume Completeness: 20%
    
    Args:
        resume_text (str): The resume text.
        job_text (str): The job description text.
    
    Returns:
        dict: A comprehensive scoring dictionary containing:
            - ats_score: Final ATS score (0-100)
            - skill_match_percentage: Skill overlap percentage
            - semantic_score: Semantic similarity score
            - completeness_score: Resume completeness score
            - semantic_label: Description of semantic match quality
            - resume_skills: Skills found in resume
            - job_skills: Skills found in job description
            - matched_skills: Skills matching between both
            - missing_skills: Skills required but not found
            - feedback_summary: Human-readable feedback
    """
    # Get skill match analysis
    skill_match = analyze_skill_match(resume_text, job_text)
    skill_match_percentage = skill_match["skill_match_percentage"]
    
    # Get semantic similarity
    semantic_data = calculate_semantic_similarity(resume_text, job_text)
    semantic_score = semantic_data["semantic_score"]
    semantic_label = semantic_data["semantic_label"]
    
    # Get completeness score
    completeness_score = calculate_completeness_score(resume_text)
    
    # Calculate weighted ATS score (0-100)
    ats_score = round(
        (skill_match_percentage * 0.5) +
        (semantic_score * 0.3) +
        (completeness_score * 0.2),
        2
    )
    
    # Generate feedback summary
    if ats_score >= 80:
        feedback_summary = "Strong match. Resume is well aligned with the job."
    elif ats_score >= 60:
        feedback_summary = "Good match. Resume is relevant but can be improved."
    elif ats_score >= 40:
        feedback_summary = "Moderate match. Resume needs stronger alignment."
    else:
        feedback_summary = "Low match. Resume needs major tailoring."
    
    return {
        "ats_score": ats_score,
        "skill_match_percentage": skill_match_percentage,
        "semantic_score": semantic_score,
        "completeness_score": completeness_score,
        "semantic_label": semantic_label,
        "resume_skills": skill_match["resume_skills"],
        "job_skills": skill_match["job_skills"],
        "matched_skills": skill_match["matched_skills"],
        "missing_skills": skill_match["missing_skills"],
        "feedback_summary": feedback_summary
    }