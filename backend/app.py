import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import ValidationError

from config import PROFILE_PATH, DATA_DIR, FRONTEND_URL
from models.career_profile import CareerProfile


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
                "http://127.0.0.1:5173"
            ]
        }
    }
)

# Limit incoming JSON request size
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024


# ==========================================
# CAREER PROFILE STORAGE
# ==========================================

def load_profile():
    """
    Load and validate the permanent career profile.
    """

    if not PROFILE_PATH.exists():
        raise FileNotFoundError(
            "Career profile file does not exist.",
            print("Career profile file does not exist at.")

        )
    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        profile_data = json.load(file)

    return CareerProfile.model_validate(profile_data)


def save_profile(profile):
    """
    Validate and save the career profile as JSON.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    profile_data = profile.model_dump(mode="json")

    with PROFILE_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            profile_data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Personal Career Agent backend is running.",
    }),print(f"Personal Career Agent backend is running. {200}")


# ==========================================
# GET CAREER PROFILE
# ==========================================

@app.route("/api/profile", methods=["GET"])
def get_profile():
    try:
        profile = load_profile()

        return jsonify({
            "status": "success",
            "profile": profile.model_dump(mode="json")
        }), 200

    except FileNotFoundError:
        return jsonify({
            "status": "error",
            "message": "Career profile file was not found."
        }), 404

    except json.JSONDecodeError:
        return jsonify({
            "status": "error",
            "message": "Career profile contains invalid JSON."
        }), 500

    except ValidationError:
        return jsonify({
            "status": "error",
            "message": "Career profile does not match the expected structure."
        }), 500

    except OSError:
        app.logger.exception("Unable to read career profile.")

        return jsonify({
            "status": "error",
            "message": "Unable to read career profile."
        }), 500


# ==========================================
# UPDATE CAREER PROFILE
# ==========================================

@app.route("/api/profile", methods=["PUT"])
def update_profile():
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request must contain JSON data."
        }), 415

    profile_data = request.get_json(silent=True)

    if not isinstance(profile_data, dict):
        return jsonify({
            "status": "error",
            "message": "A valid JSON object is required."
        }), 400

    try:
        # Validate the submitted profile
        profile = CareerProfile.model_validate(profile_data)

        # Persist the validated profile
        save_profile(profile)

        return jsonify({
            "status": "success",
            "message": "Career profile updated successfully.",
            "profile": profile.model_dump(mode="json")
        }), 200

    except ValidationError as error:
        return jsonify({
            "status": "error",
            "message": "Career profile validation failed.",
            "details": error.errors(
                include_context=False,
                include_url=False
            )
        }), 400

    except OSError:
        app.logger.exception("Unable to save career profile.")

        return jsonify({
            "status": "error",
            "message": "Unable to save career profile."
        }), 500


# ==========================================
# START DEVELOPMENT SERVER
# ==========================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )