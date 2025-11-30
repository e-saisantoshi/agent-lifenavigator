# config.py
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, we just rely on environment variables
    pass

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def ensure_api_key():
    """
    Ensure the Gemini API key is available.
    This keeps code safe and avoids hardcoding secrets.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY.strip() == "":
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Please set it as an environment "
            "variable or in a local .env file (which is NOT committed)."
        )
