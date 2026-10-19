import json
import os

from dotenv import load_dotenv
from google import genai
from pydantic import ValidationError

from models.job_description import JobDescription

load_dotenv()

def analyze_job_description(job_text: str) -> JobDescription:
    """Analyze a job advertisement using Gemini and return validated, structured job information."""

    if not isinstance(job_text, str) or not job_text.strip():
        raise ValueError("A job description must be provided.")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    ```

    You are a job advertisement analysis assistant.

    Analyze the job advertisement below and extract its information
    into a JSON object.

    Rules:

    1. Use only information supported by the advertisement.
    2. Do not invent skills, qualifications, certifications, or experience.
    3. If a field is not stated, return an empty string or empty list.
    4. Keep required skills separate from preferred skills.
    5. Extract relevant ATS keywords from the advertisement.
    6. Return valid JSON only, without Markdown code fences.
    7. Do not treat qualifications mentioned in the advertisement
    as qualifications possessed by the applicant.

    Return an object with exactly these fields:
    {{
    "job_title": "",
    "company": "",
    "location": "",
    "required_skills": [],
    "preferred_skills": [],
    "responsibilities": [],
    "qualifications": [],
    "certifications": [],
    "experience_requirements": [],
    "ats_keywords": [],
    "source_url": ""
    }}

    JOB ADVERTISEMENT:
    {job_text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.1,
            },
        )

        response_text = response.text

        if not response_text:
            raise RuntimeError("Gemini returned an empty response.")

        structured_data = json.loads(response_text)

        return JobDescription.model_validate(structured_data)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Gemini returned an invalid JSON response."
        ) from exc

    except ValidationError as exc:
        raise RuntimeError(
            "Gemini returned job information that failed validation."
        ) from exc