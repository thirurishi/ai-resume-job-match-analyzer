"""
Unit tests for ats_scorer module.
"""

import pytest
from core.scoring.ats_scorer import calculate_ats_score, calculate_completeness_score


def test_ats_score_in_range():
    """Test that ATS score is between 0 and 100."""
    resume = "Python SQL experience"
    job = "Looking for Python and SQL developer"
    result = calculate_ats_score(resume, job)
    assert 0 <= result["ats_score"] <= 100


def test_ats_result_has_required_keys():
    """Test that ATS result contains all required keys."""
    resume = "Senior developer with Python expertise"
    job = "We need a Python developer with 5 years experience"
    result = calculate_ats_score(resume, job)
    
    required_keys = [
        "ats_score",
        "skill_match_percentage",
        "semantic_score",
        "completeness_score",
        "semantic_label",
        "resume_skills",
        "job_skills",
        "matched_skills",
        "missing_skills",
        "feedback_summary"
    ]
    
    for key in required_keys:
        assert key in result, f"Missing key: {key}"


def test_skill_match_percentage_in_range():
    """Test that skill match percentage is between 0 and 100."""
    resume = "Python and SQL"
    job = "Looking for Python, SQL, and JavaScript"
    result = calculate_ats_score(resume, job)
    assert 0 <= result["skill_match_percentage"] <= 100


def test_semantic_score_in_range():
    """Test that semantic score is between 0 and 100."""
    resume = "Experienced software engineer"
    job = "Senior software engineer position"
    result = calculate_ats_score(resume, job)
    assert 0 <= result["semantic_score"] <= 100


def test_completeness_score_in_range():
    """Test that completeness score is between 0 and 100."""
    resume = "Experience Education Skills"
    job = "Looking for developer"
    result = calculate_ats_score(resume, job)
    assert 0 <= result["completeness_score"] <= 100


def test_semantic_label_valid():
    """Test that semantic label is one of expected values."""
    resume = "Python developer"
    job = "Python developer"
    result = calculate_ats_score(resume, job)
    valid_labels = ["Strong Match", "Good Match", "Moderate Match", "Low Match"]
    assert result["semantic_label"] in valid_labels


def test_feedback_summary_not_empty():
    """Test that feedback summary is not empty."""
    resume = "Software engineer"
    job = "Looking for software engineer"
    result = calculate_ats_score(resume, job)
    assert len(result["feedback_summary"]) > 0


def test_empty_resume_handled():
    """Test that empty resume is handled gracefully."""
    resume = ""
    job = "Python developer needed"
    result = calculate_ats_score(resume, job)
    assert "ats_score" in result
    assert result["skill_match_percentage"] == 0


def test_empty_job_handled():
    """Test that empty job description is handled gracefully."""
    resume = "Python expert"
    job = ""
    result = calculate_ats_score(resume, job)
    assert "ats_score" in result


def test_matched_skills_subset_of_job_skills():
    """Test that matched skills are subset of job skills."""
    resume = "Python SQL Docker"
    job = "Need Python and SQL developer"
    result = calculate_ats_score(resume, job)
    matched = set(result["matched_skills"])
    job_skills = set(result["job_skills"])
    assert matched.issubset(job_skills)


def test_missing_skills_subset_of_job_skills():
    """Test that missing skills are subset of job skills."""
    resume = "Python"
    job = "Need Python, SQL, and Docker"
    result = calculate_ats_score(resume, job)
    missing = set(result["missing_skills"])
    job_skills = set(result["job_skills"])
    assert missing.issubset(job_skills)


def test_completeness_score_calculation():
    """Test completeness score based on sections found."""
    # Resume with multiple sections
    resume = """
    Education: BS Computer Science
    Experience: 5 years as developer
    Skills: Python, SQL
    Projects: Built several apps
    Certifications: AWS Certified
    """
    result = calculate_completeness_score(resume)
    # Should find multiple sections
    assert result > 0