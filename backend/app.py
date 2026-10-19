import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import ValidationError
from werkzeug.exceptions import RequestEntityTooLarge
from services.job_description_analyzer import analyze_job_description
from services.profile_matcher import match_career_profile

from config import PROFILE_PATH, DATA_DIR, FRONTEND_URL
from models.career_profile import CareerProfile
from services.input_processor import (
    validate_job_text,
    validate_job_image,
)
from services.image_text_extractor import extract_text_from_image


# ==========================================
# INITIALIZE FLASK
# ==========================================

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                FRONTEND_URL,
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
        }
    },
)

# Maximum total request size.
# Allows multipart overhead while keeping uploads bounded.
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024


# ==========================================
# CAREER PROFILE STORAGE
# ==========================================

def load_profile():
    """Load and validate the permanent career profile."""

    if not PROFILE_PATH.exists():
        raise FileNotFoundError("Career profile file does not exist.")

    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        profile_data = json.load(file)

    return CareerProfile.model_validate(profile_data)


def save_profile(profile):
    """Validate and save the career profile as JSON."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    profile_data = profile.model_dump(mode="json")

    with PROFILE_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            profile_data,
            file,
            indent=4,
            ensure_ascii=False,
        )


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Personal Career Agent backend is running.",
    }), 200


# ==========================================
# GET CAREER PROFILE
# ==========================================

@app.route("/api/profile", methods=["GET"])
def get_profile():
    try:
        profile = load_profile()

        return jsonify({
            "status": "success",
            "profile": profile.model_dump(mode="json"),
        }), 200

    except FileNotFoundError:
        return jsonify({
            "status": "error",
            "message": "Career profile file was not found.",
        }), 404

    except json.JSONDecodeError:
        return jsonify({
            "status": "error",
            "message": "Career profile contains invalid JSON.",
        }), 500

    except ValidationError:
        return jsonify({
            "status": "error",
            "message": "Career profile does not match the expected structure.",
        }), 500

    except OSError:
        app.logger.exception("Unable to read career profile.")

        return jsonify({
            "status": "error",
            "message": "Unable to read career profile.",
        }), 500


# ==========================================
# UPDATE CAREER PROFILE
# ==========================================

@app.route("/api/profile", methods=["PUT"])
def update_profile():
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request must contain JSON data.",
        }), 415

    profile_data = request.get_json(silent=True)

    if not isinstance(profile_data, dict):
        return jsonify({
            "status": "error",
            "message": "A valid JSON object is required.",
        }), 400

    try:
        profile = CareerProfile.model_validate(profile_data)
        save_profile(profile)

        return jsonify({
            "status": "success",
            "message": "Career profile updated successfully.",
            "profile": profile.model_dump(mode="json"),
        }), 200

    except ValidationError as error:
        return jsonify({
            "status": "error",
            "message": "Career profile validation failed.",
            "details": error.errors(
                include_context=False,
                include_url=False,
            ),
        }), 400

    except OSError:
        app.logger.exception("Unable to save career profile.")

        return jsonify({
            "status": "error",
            "message": "Unable to save career profile.",
        }), 500


# ==========================================
# JOB DESCRIPTION INPUT AND OCR
# ==========================================

@app.route("/api/job-description/extract", methods=["POST"])
def extract_job_description():
    """
    Accept either:
    - JSON containing a 'text' field.
    - Multipart form data containing an 'image' file.

    Returns validated job-description text.
    """

    try:
        # --------------------------------------
        # Option 1: Job description submitted as text
        # --------------------------------------

        if request.is_json:
            data = request.get_json(silent=True)

            if not isinstance(data, dict):
                return jsonify({
                    "status": "error",
                    "message": "A valid JSON object is required.",
                }), 400

            if "text" not in data:
                return jsonify({
                    "status": "error",
                    "message": "Provide a job description in the 'text' field.",
                }), 400

            job_text = validate_job_text(data["text"])

            return jsonify({
                "status": "success",
                "source": "text",
                "job_description": job_text,
            }), 200

        # --------------------------------------
        # Option 2: Job description submitted as an image
        # --------------------------------------

        if request.mimetype == "multipart/form-data":
            uploaded_image = request.files.get("image")

            if uploaded_image is None:
                return jsonify({
                    "status": "error",
                    "message": "Upload an image using the 'image' field.",
                }), 400

            image_bytes = validate_job_image(uploaded_image)

            extracted_text = extract_text_from_image(image_bytes)

            # Apply text validation to the OCR result as well.
            job_text = validate_job_text(extracted_text)

            return jsonify({
                "status": "success",
                "source": "image",
                "job_description": job_text,
            }), 200

        return jsonify({
            "status": "error",
            "message": (
                "Unsupported request format. Submit JSON text "
                "or a multipart image upload."
            ),
        }), 415

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error),
        }), 400

    except RuntimeError:
        app.logger.exception("OCR service failed.")

        return jsonify({
            "status": "error",
            "message": "The OCR service is unavailable or failed.",
        }), 500


# ==========================================
# REQUEST SIZE ERROR HANDLER
# ==========================================

@app.errorhandler(RequestEntityTooLarge)
def handle_request_too_large(error):
    return jsonify({
        "status": "error",
        "message": "The request exceeds the maximum allowed size of 12 MB.",
    }), 413


#analyze job description 

@app.route("/api/job-description/analyze", methods=["POST"])
def analyze_job_description_endpoint():
    try:
        if not request.is_json:
            return jsonify({
                "status": "error",
                "message": "Request must contain JSON data."
            }), 415

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "status": "error",
                "message": "A valid JSON object is required."
            }), 400

        if "text" not in data:
            return jsonify({
                "status": "error",
                "message": "Provide a job description in the 'text' field."
            }), 400

        job_text = validate_job_text(data["text"])

        result = analyze_job_description(job_text)

        return jsonify({
            "status": "success",
            "job_description": result.model_dump(mode="json")
        }), 200

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except RuntimeError:
        app.logger.exception("Job description analysis failed.")
        return jsonify({
            "status": "error",
            "message": "Unable to analyze the job description."
        }), 502

    except Exception:
        app.logger.exception("Unexpected job analysis error.")
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred during job analysis."
        }), 500

#Add the matching endpoint


@app.route("/api/profile/match", methods=["POST"])
def match_profile_endpoint():
    try:
        if not request.is_json:
            return jsonify({
            "status": "error",
            "message": "Request must contain JSON data."
            }), 415


        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "status": "error",
                "message": "A valid JSON object is required."
            }), 400

        if "text" not in data:
            return jsonify({
                "status": "error",
                "message": "Provide a job description in the 'text' field."
            }), 400

        # Validate the submitted job advertisement.
        job_text = validate_job_text(data["text"])

        # Use Gemini to extract structured job information.
        job = analyze_job_description(job_text)

        # Load the applicant's actual career profile.
        profile = load_profile()

        # Compare the profile against the job requirements.
        match_result = match_career_profile(profile, job)

        return jsonify({
            "status": "success",
            "job_description": job.model_dump(mode="json"),
            "match_results": match_result
        }), 200

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except RuntimeError:
        app.logger.exception("Career profile matching failed.")
        return jsonify({
            "status": "error",
            "message": "Unable to analyze or match the job description."
        }), 502

    except Exception:
        app.logger.exception("Unexpected profile matching error.")
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred during profile matching."
        }), 500



# ==========================================
# START DEVELOPMENT SERVER
# ==========================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
