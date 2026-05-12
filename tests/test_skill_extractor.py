"""
Unit tests for skill_extractor module.
"""

import pytest
from core.scoring.skill_extractor import extract_skills


def test_python_detection():
    """Test that Python skill is detected."""
    text = "I have experience with Python programming"
    result = extract_skills(text)
    assert "Python" in result


def test_sql_detection():
    """Test that SQL skill is detected."""
    text = "Proficient in SQL and database management"
    result = extract_skills(text)
    assert "SQL" in result


def test_power_bi_detection():
    """Test that Power BI skill is detected."""
    text = "Created dashboards using Power BI"
    result = extract_skills(text)
    assert "Power BI" in result


def test_powerbi_alias_detection():
    """Test that powerbi alias is converted to Power BI."""
    text = "I am skilled in powerbi and Tableau"
    result = extract_skills(text)
    assert "Power BI" in result
    assert "Tableau" in result


def test_sklearn_alias_detection():
    """Test that sklearn alias is converted to Scikit-learn."""
    text = "Using sklearn for machine learning models"
    result = extract_skills(text)
    assert "Scikit-learn" in result


def test_postgres_alias_detection():
    """Test that postgres alias is converted to PostgreSQL."""
    text = "Experienced with postgres database systems"
    result = extract_skills(text)
    assert "PostgreSQL" in result


def test_case_insensitive():
    """Test that skill detection is case-insensitive."""
    text = "PYTHON, python, Python"
    result = extract_skills(text)
    # Should only appear once
    assert result.count("Python") <= 1


def test_no_duplicates():
    """Test that duplicate skills are not returned."""
    text = "Python Python Python SQL SQL"
    result = extract_skills(text)
    assert result.count("Python") == 1
    assert result.count("SQL") == 1


def test_sorted_output():
    """Test that output is sorted alphabetically."""
    text = "I know Tableau, Python, AWS, and Docker"
    result = extract_skills(text)
    # Check that result is sorted
    assert result == sorted(result)


def test_empty_string():
    """Test that empty string returns empty list."""
    result = extract_skills("")
    assert result == []


def test_none_value():
    """Test that None value returns empty list."""
    result = extract_skills(None)
    assert result == []


def test_multiple_skills_detection():
    """Test detection of multiple skills in one text."""
    text = "Python, SQL, Excel, FastAPI, Docker, and AWS experience"
    result = extract_skills(text)
    assert len(result) >= 4
    assert "Python" in result
    assert "SQL" in result
    assert "Docker" in result