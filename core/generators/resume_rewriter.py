"""
Resume bullet rewriter for generating ATS-friendly improvement suggestions.
"""


ACTION_VERBS = [
    "Developed", "Designed", "Implemented", "Engineered", "Created",
    "Optimized", "Improved", "Enhanced", "Streamlined", "Accelerated",
    "Automated", "Architected", "Deployed", "Integrated", "Managed",
    "Led", "Mentored", "Collaborated", "Coordinated", "Analyzed",
    "Resolved", "Pioneered", "Transformed", "Established", "Launched"
]

IMPACT_PHRASES = [
    "resulting in improved efficiency",
    "increasing performance by [X]%",
    "reducing time by [X] hours/days",
    "saving [X] resources",
    "improving accuracy to [X]%",
    "enhancing user experience",
    "enabling faster delivery",
    "supporting [X] users/clients",
    "strengthening team capabilities",
    "accelerating development cycles"
]


def generate_resume_bullets(resume_text: str, job_text: str, ats_result: dict) -> list:
    """
    Generate improved resume bullet point examples with ATS-friendly language.
    
    Args:
        resume_text (str): The resume text.
        job_text (str): The job description text.
        ats_result (dict): The ATS scoring result.
    
    Returns:
        list: List of 3-5 improved resume bullet suggestions.
    """
    bullets = []
    
    matched_skills = ats_result.get("matched_skills", [])
    job_skills = ats_result.get("job_skills", [])
    
    # Bullet 1: Using matched skills
    if matched_skills:
        skill = matched_skills[0]
        verb = ACTION_VERBS[0]
        bullets.append(
            f"{verb} and maintained solutions using {skill}, "
            "resulting in improved system reliability and performance."
        )
    
    # Bullet 2: General achievement
    bullets.append(
        "Developed scalable solutions and improved processes, "
        "resulting in [X]% efficiency gain and reduced operational costs."
    )
    
    # Bullet 3: Using second matched skill if available
    if len(matched_skills) > 1:
        skill = matched_skills[1]
        verb = ACTION_VERBS[5]  # "Optimized"
        bullets.append(
            f"{verb} existing workflows with {skill}, "
            "resulting in faster turnaround time and better resource utilization."
        )
    else:
        bullets.append(
            "Collaborated with cross-functional teams to implement improvements, "
            "supporting [X] projects and delivering on timeline."
        )
    
    # Bullet 4: Data/metrics driven
    bullets.append(
        "Analyzed performance metrics and implemented data-driven improvements, "
        "resulting in [X]% improvement in key performance indicators."
    )
    
    # Bullet 5: Using job-specific skills if available
    if job_skills and len(matched_skills) < len(job_skills):
        gap_skill = job_skills[0]
        bullets.append(
            f"Applied expertise in {gap_skill} to deliver critical features, "
            "enhancing product capability and user satisfaction."
        )
    
    # Return 3-5 bullets
    return bullets[:5]