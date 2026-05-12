"""
Cover letter generator for creating professional cover letter drafts.
"""


def generate_cover_letter(resume_text: str, job_text: str, ats_result: dict) -> str:
    """
    Generate a professional cover letter draft based on resume, job description, and ATS analysis.
    
    Args:
        resume_text (str): The resume text.
        job_text (str): The job description text.
        ats_result (dict): The ATS scoring result.
    
    Returns:
        str: A professionally formatted cover letter draft.
    """
    matched_skills = ats_result.get("matched_skills", [])
    missing_skills = ats_result.get("missing_skills", [])
    skill_match_pct = ats_result.get("skill_match_percentage", 0)
    
    # Build cover letter
    cover_letter = "Dear Hiring Manager,\n\n"
    
    # Opening paragraph
    if skill_match_pct >= 70:
        cover_letter += (
            "I am writing to express my strong interest in this position. "
            "With my background and proven expertise, I am confident I can "
            "make an immediate and meaningful contribution to your team.\n\n"
        )
    elif skill_match_pct >= 50:
        cover_letter += (
            "I am interested in this opportunity and believe my skills and experience "
            "align well with your team's needs. I am excited to learn more about this role.\n\n"
        )
    else:
        cover_letter += (
            "I am interested in this position and see strong potential for growth and learning. "
            "I am committed to quickly developing the additional expertise required.\n\n"
        )
    
    # Skills paragraph
    cover_letter += "My professional experience includes expertise in "
    if matched_skills:
        skills_str = ", ".join(matched_skills[:3])
        if len(matched_skills) > 3:
            skills_str += f", and other technologies"
        cover_letter += f"{skills_str}. "
    
    cover_letter += (
        "These skills directly align with your job requirements. "
        "Throughout my career, I have consistently delivered quality results "
        "and continuously sought to expand my technical knowledge.\n\n"
    )
    
    # Missing skills paragraph (if any)
    if missing_skills and len(missing_skills) > 0:
        cover_letter += (
            "I recognize that this role requires expertise in areas such as "
        )
        missing_str = ", ".join(missing_skills[:3])
        if len(missing_skills) > 3:
            missing_str += f", and others"
        cover_letter += (
            f"{missing_str}. While my direct experience with these is limited, "
            "I have a strong foundation and am committed to rapidly developing proficiency "
            "through dedicated learning and hands-on experience.\n\n"
        )
    
    # Closing paragraph
    cover_letter += (
        "I am enthusiastic about the opportunity to contribute to your organization "
        "and would welcome the chance to discuss how my background can benefit your team. "
        "Thank you for considering my application. I look forward to speaking with you soon.\n\n"
        "Best regards,\n"
        "[Your Name]"
    )
    
    return cover_letter