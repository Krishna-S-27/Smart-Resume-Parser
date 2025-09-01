import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY in .env file")


def parse_resume_with_ai(text):
    """
    Parse resume text using OpenRouter API (Mistral-7B free model).
    """
    schema_prompt = """
    Extract the following structured information from this resume text:

    {
      "name": "Candidate name only",
      "email": "Email address",
      "phone": "Phone number",
      "links": ["URLs like LinkedIn, GitHub, Portfolio"],
      "skills": ["Python", "Java", ...],
      "education": ["Degree, College, Year"],
      "experience": ["Work roles, internships"],
      "sections": {
          "projects": [],
          "achievements": [],
          "certificates": [],
          "hobbies": [],
          "profiles": []
      },
      "summary": "2–3 sentence professional summary"
    }

    Resume Text:
    """ + text

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer " + OPENROUTER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",  # ✅ free model
        "messages": [{"role": "user", "content": schema_prompt}]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]

    try:
        return json.loads(content)
    except Exception:
        return {"raw_output": content}