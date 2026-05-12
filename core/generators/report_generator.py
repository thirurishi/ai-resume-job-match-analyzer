"""
Report generator for creating comprehensive analysis reports.
"""

from datetime import datetime


def generate_text_report(
    resume_metrics: dict,
    job_metrics: dict,
    ats_result: dict,
    feedback: dict,
    resume_bullets: list,
    cover_letter: str,
    linkedin_message: str
) -> str:
    """
    Generate a comprehensive text report with all analysis results.
    
    Args:
        resume_metrics (dict): Resume parsing metrics
        job_metrics (dict): Job description metrics
        ats_result (dict): ATS scoring results
        feedback (dict): Recruiter feedback
        resume_bullets (list): Improved resume bullets
        cover_letter (str): Generated cover letter
        linkedin_message (str): Generated LinkedIn message
    
    Returns:
        str: A formatted text report.
    """
    report = "="*70 + "\n"
    report += "AI RESUME & JOB MATCH ANALYZER - COMPREHENSIVE ANALYSIS REPORT\n"
    report += "="*70 + "\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "="*70 + "\n\n"
    
    # Section 1: Input Metrics
    report += "1. INPUT ANALYSIS METRICS\n"
    report += "-"*70 + "\n"
    report += "Resume Metrics:\n"
    report += f"  - Word Count: {resume_metrics.get('word_count', 0)}\n"
    report += f"  - Character Count: {resume_metrics.get('character_count', 0):,}\n"
    report += f"  - Page Count: {resume_metrics.get('page_count', 0)}\n\n"
    
    report += "Job Description Metrics:\n"
    report += f"  - Word Count: {job_metrics.get('word_count', 0)}\n"
    report += f"  - Character Count: {job_metrics.get('character_count', 0):,}\n\n"
    
    # Section 2: ATS Score Breakdown
    report += "2. ATS SCORE BREAKDOWN\n"
    report += "-"*70 + "\n"
    report += f"Overall ATS Score: {ats_result.get('ats_score', 0)}/100\n"
    report += f"  - Skill Match: {ats_result.get('skill_match_percentage', 0):.1f}%\n"
    report += f"  - Semantic Similarity: {ats_result.get('semantic_score', 0):.1f}/100\n"
    report += f"  - Resume Completeness: {ats_result.get('completeness_score', 0):.1f}%\n"
    report += f"  - Semantic Label: {ats_result.get('semantic_label', 'N/A')}\n\n"
    
    # Section 3: Skill Analysis
    report += "3. SKILL ANALYSIS\n"
    report += "-"*70 + "\n"
    
    matched_skills = ats_result.get('matched_skills', [])
    report += f"Matched Skills ({len(matched_skills)}):\n"
    if matched_skills:
        for skill in matched_skills:
            report += f"  ✓ {skill}\n"
    else:
        report += "  (No matching skills found)\n"
    report += "\n"
    
    missing_skills = ats_result.get('missing_skills', [])
    report += f"Missing Skills ({len(missing_skills)}):\n"
    if missing_skills:
        for skill in missing_skills:
            report += f"  ✗ {skill}\n"
    else:
        report += "  (All required skills are present)\n"
    report += "\n"
    
    resume_skills = ats_result.get('resume_skills', [])
    report += f"Resume Skills ({len(resume_skills)}):\n"
    if resume_skills:
        report += f"  {', '.join(resume_skills)}\n"
    else:
        report += "  (No skills detected)\n"
    report += "\n"
    
    job_skills = ats_result.get('job_skills', [])
    report += f"Job Skills ({len(job_skills)}):\n"
    if job_skills:
        report += f"  {', '.join(job_skills)}\n"
    else:
        report += "  (No skills detected)\n"
    report += "\n"
    
    # Section 4: Feedback Summary
    report += "4. RECRUITER FEEDBACK\n"
    report += "-"*70 + "\n"
    report += ats_result.get('feedback_summary', 'N/A') + "\n\n"
    
    # Section 5: Strengths
    report += "5. IDENTIFIED STRENGTHS\n"
    report += "-"*70 + "\n"
    strengths = feedback.get('strengths', [])
    if strengths:
        for strength in strengths:
            report += f"  • {strength}\n"
    else:
        report += "  • Resume shows basic structure\n"
    report += "\n"
    
    # Section 6: Weaknesses
    report += "6. IDENTIFIED WEAKNESSES\n"
    report += "-"*70 + "\n"
    weaknesses = feedback.get('weaknesses', [])
    if weaknesses:
        for weakness in weaknesses:
            report += f"  • {weakness}\n"
    else:
        report += "  • No significant weaknesses identified\n"
    report += "\n"
    
    # Section 7: Improvement Suggestions
    report += "7. IMPROVEMENT SUGGESTIONS\n"
    report += "-"*70 + "\n"
    suggestions = feedback.get('suggestions', [])
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            report += f"  {i}. {suggestion}\n"
    else:
        report += "  • Continue to develop relevant skills and experience\n"
    report += "\n"
    
    # Section 8: Improved Resume Bullets
    report += "8. IMPROVED RESUME BULLET EXAMPLES\n"
    report += "-"*70 + "\n"
    if resume_bullets:
        for i, bullet in enumerate(resume_bullets, 1):
            report += f"  {i}. {bullet}\n"
    else:
        report += "  • No bullet suggestions available\n"
    report += "\n"
    
    # Section 9: Cover Letter Draft
    report += "9. COVER LETTER DRAFT\n"
    report += "-"*70 + "\n"
    report += cover_letter + "\n\n"
    
    # Section 10: LinkedIn Message Template
    report += "10. LINKEDIN MESSAGE TEMPLATE\n"
    report += "-"*70 + "\n"
    report += linkedin_message + "\n\n"
    
    # Footer
    report += "="*70 + "\n"
    report += "END OF REPORT\n"
    report += "="*70 + "\n"
    
    return report