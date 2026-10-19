import json

from models.generated_cv import (
GeneratedCV,
CVContactInfo,
CVProjectEntry,
CVEducationEntry,
)

sample_cv = GeneratedCV(
contact=CVContactInfo(
full_name="Test Candidate",
location="Johannesburg, South Africa",
email="[candidate@example.com](mailto:candidate@example.com)",
linkedin="https://www.linkedin.com/",
github="https://github.com/",
portfolio="https://example.com/",
),
professional_summary=(
"IT graduate with practical software development "
"experience and an interest in cloud computing."
),
technical_skills={
"Programming Languages": [
"Python",
"C#",
"JavaScript",
],
"Databases": [
"PostgreSQL",
"SQL Server",
],
},
soft_skills=[
"Problem-solving",
"Communication",
],
experience=[],
projects=[
CVProjectEntry(
name="Example Web Application",
description=(
"A web application built to demonstrate "
"software development skills."
),
technologies=[
"Python",
"Flask",
"PostgreSQL",
],
bullets=[
"Developed application functionality.",
"Integrated a relational database.",
],
github_url="https://github.com/",
),
],
certifications=[],
education=[
CVEducationEntry(
qualification="Example IT Qualification",
institution="Example University",
status="Completed",
),
],
)

cv_data = sample_cv.model_dump(mode="json")

print("Generated CV model validation successful.")
print(json.dumps(cv_data, indent=4))

assert cv_data["contact"]["full_name"] == "Test Candidate"
assert len(cv_data["projects"]) == 1
assert "Programming Languages" in cv_data["technical_skills"]

print("\nAll model checks passed.")
