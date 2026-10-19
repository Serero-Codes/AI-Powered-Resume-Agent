from io import BytesIO

from werkzeug.datastructures import FileStorage

from services.input_processor import (
    validate_job_text,
    validate_job_image,
)


# --------------------------------------------------
# Test 1: Valid Job Description
# --------------------------------------------------

job_text = """
Junior Cloud Engineer

Requirements:
- AWS
- Python
- Linux
- Networking
"""

result = validate_job_text(job_text)

assert result.startswith("Junior Cloud Engineer")
print("PASS: Valid job description accepted.")


# --------------------------------------------------
# Test 2: Empty Job Description
# --------------------------------------------------

try:
    validate_job_text("   ")
    raise AssertionError("Empty text should have been rejected.")
except ValueError:
    print("PASS: Empty job description rejected.")


# --------------------------------------------------
# Test 3: Valid Image
# --------------------------------------------------

# image = FileStorage(
#     stream=BytesIO(b"test image data"),
#     filename="job-poster.png",
#     content_type="image/png",
# )

# image_bytes = validate_job_image(image)

# assert image_bytes == b"test image data"

# print("PASS: Image input accepted by the initial validator.")

from io import BytesIO 
from PIL import Image 
from werkzeug.datastructures import FileStorage 

buffer = BytesIO() 
test_image = Image.new("RGB", (300, 150), color=(255, 255, 255)) 
test_image.save(buffer, format="PNG") 

# Retrieve the actual PNG bytes. 

image_bytes = buffer.getvalue() 

# Confirm that Pillow can open the generated image. 
with Image.open(BytesIO(image_bytes)) as check_image: 
    print("Generated image format:", check_image.format) 
    print("Generated image dimensions:", check_image.size) 

# Simulate an uploaded image. 
uploaded_image = FileStorage( 
    stream=BytesIO(image_bytes), 
    filename="job_advertisement.png", 
    content_type="image/png", 
) 

# Run the image validator. 
validated_bytes = validate_job_image(uploaded_image) 
assert validated_bytes == image_bytes 
print("PASS: Valid PNG images are accepted.")


# --------------------------------------------------
# Test 4: Unsupported File Extension
# --------------------------------------------------

document = FileStorage(
    stream=BytesIO(b"document data"),
    filename="job-description.pdf",
    content_type="application/pdf",
)

try:
    validate_job_image(document)
    raise AssertionError("PDF should have been rejected.")
except ValueError:
    print("PASS: Unsupported file extension rejected.")


print("\nAll initial input validation tests passed.")
