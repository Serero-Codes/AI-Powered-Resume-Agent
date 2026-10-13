from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


# --------------------------------------------------
# Base Model
# Defines common validation behaviour.
# --------------------------------------------------

class StrictBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )


# --------------------------------------------------
# Personal Details
# --------------------------------------------------

class PersonalDetails(StrictBaseModel):
    full_name: str = "Serero Immanuel Mokwena"
    email: str = "sereroemmanuel4@gmail.com"
    phone: str = "076 533 4475"
    location: str = "Johannesburg, Gauteng"
    linkedin: str = "www.linkedin.com/in/serero-mokwena-3577b3347"
    github: str = "https://github.com/Serero-Codes"
    portfolio: str = "https://sererom.onrender.com/"


# --------------------------------------------------
# Skills
# --------------------------------------------------

class SkillCategories(StrictBaseModel):
    programming_languages: list[str] = Field(default_factory=list)
    cloud: list[str] = Field(default_factory=list)
    databases: list[str] = Field(default_factory=list)
    networking: list[str] = Field(default_factory=list)
    ai_and_machine_learning: list[str] = Field(default_factory=list)
    devops: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    other: list[str] = Field(default_factory=list)

    @field_validator("*")
    @classmethod
    def remove_empty_skills(cls, skills: list[str]) -> list[str]:
        return [skill.strip() for skill in skills if skill.strip()]


# --------------------------------------------------
# Education
# --------------------------------------------------

class Education(StrictBaseModel):
    name: str = ""
    institution: str = ""
    qualification: str = ""
    field_of_study: str = ""
    start_date: str = ""
    end_date: str = ""
    status: str = ""
    description: str = ""


# --------------------------------------------------
# Employment Experience
# --------------------------------------------------

class Experience(StrictBaseModel):
    role: str = ""
    company: str = ""
    period: str = ""
    location: str = ""
    employment_type: str = ""
    highlights: list[str] = Field(default_factory=list)


# --------------------------------------------------
# Projects
# --------------------------------------------------

class Project(StrictBaseModel):
    name: str = ""
    technologies: list[str] = Field(default_factory=list)
    description: str = ""
    highlights: list[str] = Field(default_factory=list)
    url: str = ""


# --------------------------------------------------
# Certifications, Courses and Achievements
# --------------------------------------------------

class Certification(StrictBaseModel):
    name: str = ""
    issuer: str = ""
    date: str = ""
    credential_id: str = ""
    credential_url: str = ""


class Course(StrictBaseModel):
    name: str = ""
    provider: str = ""
    date: str = ""
    description: str = ""


class Achievement(StrictBaseModel):
    name: str = ""
    organization: str = ""
    date: str = ""
    description: str = ""


class ProfessionalDevelopment(StrictBaseModel):
    name: str = ""
    provider: str = ""
    date: str = ""
    description: str = ""


# --------------------------------------------------
# Main Career Profile
# --------------------------------------------------

class CareerProfile(StrictBaseModel):
    personal: PersonalDetails = Field(default_factory=PersonalDetails)

    professional_summary: str = ""

    career_objectives: list[str] = Field(default_factory=list)

    education: list[Education] = Field(default_factory=list)

    experience: list[Experience] = Field(default_factory=list)

    projects: list[Project] = Field(default_factory=list)

    skills: SkillCategories = Field(default_factory=SkillCategories)

    certifications: list[Certification] = Field(default_factory=list)

    courses: list[Course] = Field(default_factory=list)

    achievements: list[Achievement] = Field(default_factory=list)

    interests: list[str] = Field(default_factory=list)

    professional_development: list[ProfessionalDevelopment] = Field(
        default_factory=list
    )

    languages: list[str] = Field(default_factory=list)

    additional_information: list[str] = Field(default_factory=list)
