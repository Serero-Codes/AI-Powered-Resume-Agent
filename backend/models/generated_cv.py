from pydantic import BaseModel, ConfigDict, Field


class CVBaseModel(BaseModel):
    """Shared validation rules for generated CV data."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

class CVContactInfo(CVBaseModel):
    """Contact details displayed in the CV header."""

    full_name: str
    location: str = ""
    phone: str = ""
    email: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""

class CVExperienceEntry(CVBaseModel):
    """A work experience or internship entry."""

    job_title: str
    organization: str
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    bullets: list[str] = Field(default_factory=list)

class CVProjectEntry(CVBaseModel):
    """A technical or professional project."""

    name: str
    description: str = ""
    technologies: list[str] = Field(default_factory=list)
    bullets: list[str] = Field(default_factory=list)
    github_url: str = ""
    demo_url: str = ""

class CVEducationEntry(CVBaseModel):
    """An educational qualification."""

    qualification: str
    institution: str
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    status: str = ""

class CVCertificationEntry(CVBaseModel):
    """A certification or relevant professional course."""

    name: str
    issuer: str = ""
    date: str = ""
    status: str = ""


class GeneratedCV(CVBaseModel):
    """Structured content for a job-specific CV."""

    contact: CVContactInfo
    professional_summary: str

    technical_skills: dict[str, list[str]] = Field(default_factory=dict)

    soft_skills: list[str] = Field(default_factory=list)

    experience: list[CVExperienceEntry] = Field(default_factory=list)

    projects: list[CVProjectEntry] = Field(default_factory=list)

    certifications: list[CVCertificationEntry] = Field(default_factory=list)

    education: list[CVEducationEntry] = Field(default_factory=list)
