from pathlib import Path
from io import BytesIO
import warnings

from PIL import Image, UnidentifiedImageError
from werkzeug.datastructures import FileStorage


# --------------------------------------------------
# Input Validation Configuration
# --------------------------------------------------

MAX_TEXT_LENGTH = 100_000
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_IMAGE_PIXELS = 25_000_000  # 25 megapixels

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
ALLOWED_IMAGE_FORMATS = {"PNG", "JPEG"}


# --------------------------------------------------
# Text Input Validation
# --------------------------------------------------

def validate_job_text(text: str) -> str:
    """Validate a job description submitted as text."""

    if not isinstance(text, str):
        raise ValueError("Job description must be text.")

    cleaned_text = text.strip()

    if not cleaned_text:
        raise ValueError("Please provide a job description.")

    if len(cleaned_text) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"Job description exceeds the maximum length "
            f"of {MAX_TEXT_LENGTH:,} characters."
        )

    return cleaned_text


# --------------------------------------------------
# Image Input Validation
# --------------------------------------------------

def validate_job_image(image: FileStorage) -> bytes:
    """
    Validate an uploaded image by extension, actual format,
    file size, and pixel dimensions.

    Returns:
        Validated raw image bytes.

    Raises:
        ValueError: If the uploaded image is invalid.
    """

    if image is None or not image.filename:
        raise ValueError("Please upload a job advertisement image.")

    extension = Path(image.filename).suffix.lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError(
            "Unsupported image format. Upload PNG, JPG, or JPEG."
        )

    image_bytes = image.stream.read(MAX_IMAGE_SIZE + 1)

    if not image_bytes:
        raise ValueError("The uploaded image is empty.")

    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise ValueError("The image exceeds the maximum size of 10 MB.")

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)

            with Image.open(BytesIO(image_bytes)) as img:
                if img.format not in ALLOWED_IMAGE_FORMATS:
                    raise ValueError(
                        "The uploaded file is not a supported image."
                    )

                width, height = img.size

                if width * height > MAX_IMAGE_PIXELS:
                    raise ValueError(
                        "The image dimensions are too large. "
                        "Upload an image with 25 megapixels or fewer."
                    )

                img.verify()

    except ValueError:
        raise

    except (
        UnidentifiedImageError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
        OSError,
        SyntaxError,
    ) as exc:
        raise ValueError(
            "The uploaded file is not a valid image or is corrupted."
        ) from exc

    finally:
        image.stream.seek(0)

    return image_bytes