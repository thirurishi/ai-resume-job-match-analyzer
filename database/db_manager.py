"""
Database manager for SQLite persistence of analysis history.
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "analysis_history.db"


def init_db():
    """Initialize SQLite database with analysis_history table."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resume_filename TEXT NOT NULL,
                job_text TEXT,
                ats_score REAL,
                skill_match_percentage REAL,
                semantic_score REAL,
                completeness_score REAL,
                matched_skills TEXT,
                missing_skills TEXT,
                report_text TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        return False


def save_analysis(
    resume_filename: str,
    job_text: str,
    ats_score: float,
    skill_match_percentage: float,
    semantic_score: float,
    completeness_score: float,
    matched_skills: list,
    missing_skills: list,
    report_text: str
) -> bool:
    """
    Save an analysis to the database.
    
    Args:
        resume_filename (str): Name of the uploaded resume file
        job_text (str): The job description text
        ats_score (float): ATS score (0-100)
        skill_match_percentage (float): Skill match percentage
        semantic_score (float): Semantic similarity score
        completeness_score (float): Resume completeness score
        matched_skills (list): List of matched skills
        missing_skills (list): List of missing skills
        report_text (str): Full analysis report text
    
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Convert lists to comma-separated strings
        matched_skills_str = ",".join(matched_skills) if matched_skills else ""
        missing_skills_str = ",".join(missing_skills) if missing_skills else ""
        
        cursor.execute("""
            INSERT INTO analysis_history (
                resume_filename,
                job_text,
                ats_score,
                skill_match_percentage,
                semantic_score,
                completeness_score,
                matched_skills,
                missing_skills,
                report_text
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            resume_filename,
            job_text[:500],  # Store only first 500 chars of job text
            ats_score,
            skill_match_percentage,
            semantic_score,
            completeness_score,
            matched_skills_str,
            missing_skills_str,
            report_text
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving analysis: {str(e)}")
        return False


def get_analysis_history(limit: int = 5) -> list:
    """
    Retrieve recent analysis history from database.
    
    Args:
        limit (int): Maximum number of records to retrieve (default: 5)
    
    Returns:
        list: List of analysis records as dictionaries
    """
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM analysis_history
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert rows to dictionaries
        analyses = []
        for row in rows:
            analysis = {
                "id": row["id"],
                "created_at": row["created_at"],
                "resume_filename": row["resume_filename"],
                "ats_score": row["ats_score"],
                "skill_match_percentage": row["skill_match_percentage"],
                "semantic_score": row["semantic_score"],
                "completeness_score": row["completeness_score"],
                "matched_skills": row["matched_skills"].split(",") if row["matched_skills"] else [],
                "missing_skills": row["missing_skills"].split(",") if row["missing_skills"] else [],
                "report_text": row["report_text"]
            }
            analyses.append(analysis)
        
        return analyses
    except Exception as e:
        print(f"Error retrieving analysis history: {str(e)}")
        return []


def delete_analysis(analysis_id: int) -> bool:
    """Delete a single analysis record by ID."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM analysis_history WHERE id = ?", (analysis_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
    except Exception as e:
        print(f"Error deleting analysis record: {str(e)}")
        return False
