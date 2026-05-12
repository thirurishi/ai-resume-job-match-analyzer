"""
Feedback generator for recruiter insights and analysis.
"""


def generate_feedback(ats_result: dict) -> dict:
    """
    Generate recruiter feedback including strengths, weaknesses, and suggestions.
    
    Args:
        ats_result (dict): The ATS scoring result from ats_scorer.
    
    Returns:
        dict: A dictionary containing:
            - strengths: List of resume strengths
            - weaknesses: List of identified weaknesses
            - suggestions: List of improvement suggestions
    """
    strengths = []
    weaknesses = []
    suggestions = []
    
    # Analyze based on ATS score and components
    ats_score = ats_result.get("ats_score", 0)
    skill_match = ats_result.get("skill_match_percentage", 0)
    semantic_score = ats_result.get("semantic_score", 0)
    completeness = ats_result.get("completeness_score", 0)
    matched_skills = ats_result.get("matched_skills", [])
    missing_skills = ats_result.get("missing_skills", [])
    
    # Determine strengths
    if skill_match >= 70:
        strengths.append("Strong skill alignment with job requirements")
    elif skill_match >= 50:
        strengths.append("Moderate skill alignment with job requirements")
    
    if semantic_score >= 70:
        strengths.append("Resume content highly relevant to the position")
    
    if completeness >= 80:
        strengths.append("Resume includes all major sections")
    
    if matched_skills:
        strengths.append(f"Contains {len(matched_skills)} relevant skills for the role")
    
    # Determine weaknesses
    if skill_match < 50:
        weaknesses.append("Limited overlap between resume and job skills")
    
    if semantic_score < 50:
        weaknesses.append("Resume lacks sufficient relevance to job description")
    
    if completeness < 60:
        weaknesses.append("Missing key resume sections")
    
    if missing_skills:
        weaknesses.append(f"Missing {len(missing_skills)} important skills")
    
    # Generate suggestions
    if missing_skills and len(missing_skills) > 0:
        skills_str = ", ".join(missing_skills[:3])
        if len(missing_skills) > 3:
            skills_str += f", and {len(missing_skills) - 3} more"
        suggestions.append(f"Highlight or develop expertise in: {skills_str}")
    
    if semantic_score < 70:
        suggestions.append("Use more job-specific keywords and terminology in resume")
    
    if completeness < 80:
        suggestions.append("Ensure all major sections are clearly labeled")
    
    if skill_match < 70:
        suggestions.append("Tailor resume to emphasize relevant technical skills")
    
    if ats_score < 60:
        suggestions.append("Consider a significant resume redesign to improve alignment")
    
    suggestions.append("Add quantifiable achievements and metrics where possible")
    
    # Ensure we have at least some feedback
    if not strengths:
        strengths.append("Resume shows basic structure and content")
    
    if not weaknesses:
        weaknesses.append("Room for improvement in various areas")
    
    if not suggestions:
        suggestions.append("Continue to develop relevant skills and experience")
    
    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }