from io import BytesIO

import pytesseract
from PIL import Image, ImageOps, UnidentifiedImageError


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from a job advertisement image using Tesseract OCR.

    Args:
        image_bytes: Raw bytes from a validated image.

    Returns:
        Extracted text.

    Raises:
        ValueError: If the image is invalid or contains no readable text.
        RuntimeError: If the OCR engine is unavailable or fails.
    """

    try:
        with Image.open(BytesIO(image_bytes)) as source:
            image = ImageOps.exif_transpose(source)
            image.load()

            # Convert to RGB so OCR receives a predictable image format.
            image = image.convert("RGB")

            extracted_text = pytesseract.image_to_string(
                image,
                config="--psm 6",
            ).strip()

    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(
            "Unable to read the uploaded job advertisement image."
        ) from exc

    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract OCR is not installed or its executable "
            "cannot be found. Install Tesseract and configure its path."
        ) from exc

    except pytesseract.TesseractError as exc:
        raise RuntimeError("OCR failed while processing the image.") from exc

    if not extracted_text:
        raise ValueError(
            "No readable text was detected. Try a clearer image."
        )

    return extracted_text