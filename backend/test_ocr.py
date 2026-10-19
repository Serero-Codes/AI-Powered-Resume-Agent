from io import BytesIO

from PIL import Image, ImageDraw
import pytesseract
from services.image_text_extractor import extract_text_from_image

# Configure the path to the installed Tesseract OCR executable.
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Create a sample job advertisement image.
image = Image.new("RGB", (1000, 400), "white")
draw = ImageDraw.Draw(image)

draw.text((30, 30), "Cloud Engineer", fill="black")
draw.text((30, 100), "Required Skills:", fill="black")
draw.text((30, 150), "AWS, Python, Docker and Linux", fill="black")
draw.text((30, 200), "Experience with cloud infrastructure.", fill="black")

# Convert the image into PNG bytes.
buffer = BytesIO()
image.save(buffer, format="PNG")
image_bytes = buffer.getvalue()

# Extract text using your OCR service.
extracted_text = extract_text_from_image(image_bytes)

print("\n--- EXTRACTED TEXT ---")
print(extracted_text)

# Verify that important text was detected.
assert "Cloud Engineer" in extracted_text, "Job title was not recognised."
assert "Python" in extracted_text, "Python was not recognised."

print("\nSUCCESS: OCR extracted the expected text.")