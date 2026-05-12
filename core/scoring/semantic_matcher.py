"""
Semantic matching utilities for the AI Resume & Job Match Analyzer.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_semantic_similarity(resume_text: str, job_text: str) -> dict:
    """
    Calculate semantic similarity between resume and job description
    using TF-IDF and cosine similarity.
    
    Args:
        resume_text (str): The resume text.
        job_text (str): The job description text.
    
    Returns:
        dict: A dictionary containing:
            - semantic_score: Similarity score (0-100)
            - semantic_label: Label describing the similarity level
    """
    if not resume_text or not job_text:
        return {
            "semantic_score": 0.0,
            "semantic_label": "Low Match"
        }
    
    try:
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            stop_words='english',
            lowercase=True,
            max_features=500,
            ngram_range=(1, 2)
        )
        
        # Fit and transform both texts
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Convert to 0-100 scale
        semantic_score = round(similarity * 100, 2)
        
        # Determine label based on score
        if semantic_score >= 80:
            semantic_label = "Strong Match"
        elif semantic_score >= 60:
            semantic_label = "Good Match"
        elif semantic_score >= 40:
            semantic_label = "Moderate Match"
        else:
            semantic_label = "Low Match"
        
        return {
            "semantic_score": semantic_score,
            "semantic_label": semantic_label
        }
    
    except Exception as e:
        return {
            "semantic_score": 0.0,
            "semantic_label": "Low Match"
        }