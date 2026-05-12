"""
LinkedIn message generator for creating recruiter outreach templates.
"""


def generate_linkedin_message(ats_result: dict) -> str:
    """
    Generate a LinkedIn connection/message template for recruiting outreach.
    
    Args:
        ats_result (dict): The ATS scoring result.
    
    Returns:
        str: A professionally formatted LinkedIn message template.
    """
    matched_skills = ats_result.get("matched_skills", [])
    ats_score = ats_result.get("ats_score", 0)
    
    message = "Hi [Recruiter Name],\n\n"
    
    # Opening
    message += "I hope this message finds you well. "
    
    # Skill highlight
    if matched_skills:
        skills_str = ", ".join(matched_skills[:2])
        if len(matched_skills) > 2:
            skills_str += ", and other relevant technologies"
        message += f"I have a strong background in {skills_str}. "
    
    message += "I am actively exploring new opportunities where I can "
    "contribute meaningfully and continue growing my expertise.\n\n"
    
    # Interest in opportunity
    if ats_score >= 70:
        message += (
            "I noticed your recent opening and believe my background is a strong fit "
            "for what you are looking for. "
        )
    elif ats_score >= 50:
        message += (
            "I saw your recent posting and think there could be a good match for a discussion. "
        )
    else:
        message += (
            "I am interested in learning more about opportunities within your team and "
            "how I might contribute. "
        )
    
    message += (
        "I would welcome the opportunity to discuss how my experience "
        "can benefit your organization.\n\n"
    )
    
    # Closing
    message += (
        "Would you be open to a brief conversation? "
        "I am happy to work around your schedule.\n\n"
        "Thank you for considering this opportunity.\n\n"
        "Best regards,\n"
        "[Your Name]\n"
        "[Your Title]\n"
        "[LinkedIn Profile URL]"
    )
    
    return message