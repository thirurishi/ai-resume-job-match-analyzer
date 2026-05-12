"""
Match engine for analyzing skill overlap between resume and job description.
"""

from core.scoring.skill_extractor import extract_skills


def analyze_skill_match(resume_text: str, job_text: str) -> dict:
    """
    Analyze the skill match between a resume and job description.
    
    Args:
        resume_text (str): The resume text.
        job_text (str): The job description text.
    
    Returns:
        dict: A dictionary containing:
            - resume_skills: List of skills found in resume
            - job_skills: List of skills found in job description
            - matched_skills: Skills found in both resume and job
            - missing_skills: Skills in job but not in resume
            - skill_match_percentage: Percentage of job skills found in resume
    """
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)
    
    # Find matched skills (intersection)
    matched_skills = sorted(list(set(resume_skills) & set(job_skills)))
    
    # Find missing skills (in job but not in resume)
    missing_skills = sorted(list(set(job_skills) - set(resume_skills)))
    
    # Calculate skill match percentage
    if len(job_skills) > 0:
        skill_match_percentage = (len(matched_skills) / len(job_skills)) * 100
    else:
        skill_match_percentage = 0.0
    
    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percentage": round(skill_match_percentage, 2)
    }