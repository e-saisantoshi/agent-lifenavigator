# gemini_agent.py
import google.generativeai as genai
from config import GEMINI_API_KEY, ensure_api_key

# Using latest experimental Pro model
GEMINI_MODEL_NAME = "gemini-2.0-pro-exp"


def init_gemini():
    """Configure and return a Gemini model client."""
    ensure_api_key()
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(GEMINI_MODEL_NAME)


def llm(prompt: str) -> str:
    """
    Generic wrapper for sending a prompt to Gemini 2.0 Pro Experimental.
    Returns plain text.
    """
    model = init_gemini()
    response = model.generate_content(prompt)
    return response.text.strip()
