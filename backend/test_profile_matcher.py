import json

from config import PROFILE_PATH
from models.career_profile import CareerProfile
from models.job_description import JobDescription
from services.profile_matcher import match_career_profile

# Load and validate the real career profile.

with PROFILE_PATH.open("r", encoding="utf-8") as file:
    profile_data = json.load(file)

profile = CareerProfile.model_validate(profile_data)

# Create a sample job advertisement.

job = JobDescription(
job_title="Junior Cloud Engineer",
company="Example Cloud Solutions",
required_skills=["AWS", "Python", "Linux", "Terraform"],
preferred_skills=["Docker", "Git"],
)

# Compare the career profile with the job.

result = match_career_profile(profile, job)

# Display the results.

print("\nCAREER PROFILE MATCH RESULTS")
print("=" * 40)
print(json.dumps(result, indent=4))
