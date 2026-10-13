from pydantic import Field, model_validator

from models.career_profile import StrictBaseModel


class JobDescription(StrictBaseModel):
    job_title: str = ""
    company: str = ""
    location: str = ""

    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)

    responsibilities: list[str] = Field(default_factory=list)

    qualifications: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)

    experience_requirements: list[str] = Field(default_factory=list)

    ats_keywords: list[str] = Field(default_factory=list)

    source_url: str = ""

    @model_validator(mode="after")
    def validate_job_description(self):
        if not any([
            self.job_title,
            self.company,
            self.required_skills,
            self.preferred_skills,
            self.responsibilities,
            self.qualifications,
            self.experience_requirements,
        ]):
            raise ValueError(
                "The job description contains no meaningful job information."
            )

        return self