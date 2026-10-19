from services.job_description_analyzer import analyze_job_description

sample_job = """
Job Title: Junior Cloud Engineer
Company: Example Cloud Solutions
Location: Johannesburg, South Africa

Responsibilities:

* Assist with deploying cloud infrastructure.
* Monitor cloud resources.
* Troubleshoot infrastructure issues.

Required Skills:

* AWS
* Linux
* Networking
* Python

Preferred Skills:

* Terraform
* Docker

Qualifications:

* Diploma or degree in IT or a related field.

Experience:

* Familiarity with cloud computing concepts.
  """

try:
  result = analyze_job_description(sample_job)

  print("\nJOB ANALYSIS SUCCESSFUL")
  print(result.model_dump_json(indent=2))

except Exception as error:
  print(f"\nJOB ANALYSIS FAILED: {error}")
