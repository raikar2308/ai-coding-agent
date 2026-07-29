"""
config.py

Loads environment variables and initializes Gemini.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "models/gemini-2.0-flash")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found.\n"
        "Create a .env file and add:\n"
        "GEMINI_API_KEY=your_api_key"
    )

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)