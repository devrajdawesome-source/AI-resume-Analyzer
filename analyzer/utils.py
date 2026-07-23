import json
import os
from google import genai
from google.genai import types

def calculate_ats_score(resume_text: str, job_description_text: str) -> dict:
    """
    Sends resume text and job description to Google Gemini API to get a universal,
    domain-agnostic ATS evaluation, missing skills, and actionable feedback.
    """
    if not job_description_text.strip() or not resume_text.strip():
        return {
            "match_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "suggestions": ["Please provide both a resume and a job description."],
            "message": "Empty resume or job description provided."
        }

    # Retrieve API key from environment variables (or fall back to string during testing)
    api_key = os.getenv("GEMINI_API_KEY")
    try:
        # Initialize Gemini Client
        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are an expert ATS (Applicant Tracking System) recruiter and hiring manager.
        Analyze the following Resume against the provided Job Description.

        --- JOB DESCRIPTION ---
        {job_description_text}

        --- RESUME ---
        {resume_text}

        Evaluate the fit regardless of industry/domain (tech, finance, healthcare, marketing, etc.).
        Return your response strictly as valid JSON with the following exact keys:
        - "match_score": Integer between 0 and 100 representing overall suitability.
        - "matching_skills": List of strings representing skills, tools, or qualifications present in both.
        - "missing_skills": List of key required skills, tools, or domain knowledge missing from the resume.
        - "suggestions": List of 2-3 short, actionable bullet points to improve the resume for this specific job.
        """

        # Enforce structured JSON response schema from Gemini
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )

        # Parse JSON string returned by Gemini
        result = json.loads(response.text)

        return {
            "match_score": int(result.get("match_score", 0)),
            "matching_skills": result.get("matching_skills", []),
            "missing_skills": result.get("missing_skills", []),
            "suggestions": result.get("suggestions", [])
        }

    except Exception as e:
        print("Gemini API Error:", e)
        # Fallback dictionary if API fails or quota is exceeded
        return {
            "match_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "suggestions": [f"API Error: {str(e)}"],
            "message": "Failed to analyze via Gemini API."
        }