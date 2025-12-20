import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

COUNCIL_MODELS = [
    "google/gemini-2.5-flash"
]

CHAIRMAN_MODEL = "google/gemini-2.5-flash"
