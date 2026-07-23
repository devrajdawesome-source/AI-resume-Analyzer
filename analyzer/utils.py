import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Expanded tech taxonomy dictionary
TECH_KEYWORDS = {
    "python", "django", "fastapi", "flask", "react", "javascript", "typescript",
    "html", "css", "sql", "postgresql", "mysql", "mongodb", "c++", "java",
    "dsa", "git", "github", "docker", "aws", "rest", "api", "apis", "full stack",
    "frontend", "backend", "machine learning", "nlp", "pandas", "numpy", "redux",
    "express", "node", "kubernetes", "ci/cd", "microservices", "system design"
}

def clean_and_tokenize(text: str) -> list[str]:
    """Cleans text and extracts clean words."""
    cleaned = re.sub(r'[^a-zA-Z0-9\s#+]', ' ', text.lower())
    return cleaned.split()

def calculate_ats_score(resume_text: str, job_description_text: str) -> dict:
    """
    Computes ATS score using TF-IDF Vectorization + Cosine Similarity,
    and extracts key matching/missing terms weighted by JD frequency.
    """
    if not job_description_text.strip() or not resume_text.strip():
        return {
            "match_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "message": "Empty resume or job description provided."
        }

    # --- 1. TF-IDF COSINE SIMILARITY SCORE ---
    # Create the TF-IDF Vectorizer (filtering out common English stop words like 'and', 'the')
    vectorizer = TfidfVectorizer(stop_words='english')
    
    # Transform raw texts into numerical TF-IDF feature vectors
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description_text])
    
    # Calculate Cosine Similarity between vector 0 (Resume) and vector 1 (JD)
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    raw_similarity = similarity_matrix[0][0] # Value between 0.0 and 1.0
    
    # Scale to percentage (e.g., 0.65 -> 65%)
    cosine_score = int(raw_similarity * 100)

    # --- 2. FREQUENCY-DRIVEN KEYWORD MATCHING ---
    resume_words = set(clean_and_tokenize(resume_text))
    jd_words = clean_and_tokenize(job_description_text)
    
    # Count frequency of tech keywords in the JD
    jd_tech_freq = {}
    for word in jd_words:
        if word in TECH_KEYWORDS:
            jd_tech_freq[word] = jd_tech_freq.get(word, 0) + 1

    # If no standard tech keywords were found, fall back to general unique words
    if not jd_tech_freq:
        jd_tech_freq = {word: 1 for word in set(jd_words) if len(word) > 3}

    # Sort JD skills by importance (frequency)
    sorted_jd_skills = sorted(jd_tech_freq.keys(), key=lambda w: jd_tech_freq[w], reverse=True)

    matching_skills = [skill for skill in sorted_jd_skills if skill in resume_words]
    missing_skills = [skill for skill in sorted_jd_skills if skill not in resume_words]

    # Combine Cosine Similarity with Skill Match Ratio for a balanced ATS score
    skill_match_ratio = len(matching_skills) / len(sorted_jd_skills) if sorted_jd_skills else 0
    final_score = int((cosine_score * 0.6) + ((skill_match_ratio * 100) * 0.4))

    return {
        "match_score": min(final_score, 100),
        "cosine_similarity_percent": cosine_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }