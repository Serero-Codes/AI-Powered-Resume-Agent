import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY was not loaded from .env")
    raise SystemExit(1)

url = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-2.5-flash:generateContent"
)

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Reply with exactly: Gemini connection successful."
                }
            ]
        }
    ]
}

request = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    },
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
        print("HTTP status:", response.status)
        print("Gemini response:")
        print(
            result["candidates"][0]["content"]["parts"][0]["text"]
        )

except urllib.error.HTTPError as error:
    print("HTTP status:", error.code)
    print("API error:")
    print(error.read().decode("utf-8"))

except urllib.error.URLError as error:
    print("Connection error:", error.reason)
