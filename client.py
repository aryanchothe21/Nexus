import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def aiProcess(command):

    print("Sending request to Gemini...")

    response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=command,
    config=types.GenerateContentConfig(
        system_instruction="""
You are NEXAS, a virtual assistant.

Give short, clear and useful answers.
Keep responses short because they will be spoken aloud.
"""
    )
)

    print("Response received.")

    return response.text