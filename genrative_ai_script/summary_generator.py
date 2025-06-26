import json
from pathlib import Path
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini with API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")
genai.configure(api_key=api_key)

# Load JSON from file
def load_data(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Optional: list available models
def print_available_models():
    models = list(genai.list_models())
    print("Available models:")
    for m in models:
        print(f"- {m.name}")
    return [m.name for m in models]

# Generate AI summary using Gemini Flash (2.5)
def generate_ai_summary(data: dict) -> str:
    model_name = "models/gemini-2.5-flash"
    print(f"Using model: {model_name}")
    model = genai.GenerativeModel(model_name)

    prompt = (
        "You are a corporate compliance assistant. "
        "Given the following JSON extracted from an Indian ROC Form ADT-1 filing, generate a professional, concise summary. "
        "The summary should explain the appointment of the auditor, highlight any key information (such as auditor details, appointment dates, term, and auditor firm), and mention if any attachments are included. "
        "Ensure the tone is formal and suitable for corporate reporting or board communication.\n\n"
        f"{json.dumps(data, indent=2)}\n\n"
        "Summary:"
    )

    response = model.generate_content(prompt)
    return response.text.strip()
