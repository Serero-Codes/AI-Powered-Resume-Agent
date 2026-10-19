import re

from models.career_profile import CareerProfile
from models.job_description import JobDescription


def normalize_text(value: str) -> str:
    """Normalize text for consistent comparisons."""
    return re.sub(r"\s+", " ", value.strip().lower())


def collect_profile_skills(profile: CareerProfile) -> set[str]:
    """Collect skills explicitly listed in the career profile."""
    skills = set()

    for category in profile.skills.model_dump().values():
        if isinstance(category, list):
            for skill in category:
                if isinstance(skill, str) and skill.strip():
                    skills.add(normalize_text(skill))

    return skills


def match_career_profile(
    profile: CareerProfile,
    job: JobDescription,
) -> dict:
    """
    Compare the career profile against a job description.

    This initial version matches explicitly listed skills only.
    It does not infer skills from work experience or projects.
    """

    profile_skills = collect_profile_skills(profile)

    required_skills = {
        normalize_text(skill)
        for skill in job.required_skills
        if skill.strip()
    }

    preferred_skills = {
        normalize_text(skill)
        for skill in job.preferred_skills
        if skill.strip()
    }

    matched_required = sorted(profile_skills & required_skills)
    missing_required = sorted(required_skills - profile_skills)

    matched_preferred = sorted(profile_skills & preferred_skills)
    missing_preferred = sorted(preferred_skills - profile_skills)

    total_required = len(required_skills)
    total_preferred = len(preferred_skills)

    required_score = (
        len(matched_required) / total_required * 100
        if total_required
        else None
    )

    preferred_score = (
        len(matched_preferred) / total_preferred * 100
        if total_preferred
        else None
    )

    return {
        "required_skills": {
            "matched": matched_required,
            "missing": missing_required,
            "score": round(required_score, 2)
            if required_score is not None else None,
        },
        "preferred_skills": {
            "matched": matched_preferred,
            "missing": missing_preferred,
            "score": round(preferred_score, 2)
            if preferred_score is not None else None,
        },
        "overall_skill_match": {
            "score": round(
                (
                    len(matched_required) + len(matched_preferred)
                )
                / (total_required + total_preferred) * 100,
                2,
            )
            if total_required + total_preferred else None,
        },
    }