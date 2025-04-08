import os
import subprocess
import requests
import json
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# --- CONFIG ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_API_ENDPOINT = (
    "https://shrutiaiinstance.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"
)

HEADERS = {
    "Content-Type": "application/json",
    "api-key": OPENAI_API_KEY
}

def get_latest_commit_diff():
    """Get file-level changes from the latest commit."""
    try:
        diff = subprocess.check_output(
            ["git", "show", "HEAD", "--name-status", "--no-color"]
        ).decode("utf-8")
        return diff.strip()
    except subprocess.CalledProcessError as e:
        print("Error fetching latest commit diff:", e)
        return ""

def generate_pr_description(diff_text):
    """Generate PR description using Azure OpenAI."""
    prompt = f"""
You're an AI assistant that generates GitHub Pull Request descriptions.

Based on the following file changes from a commit:

{diff_text}

Write a clear, concise, and professional PR description that:
- Explains the purpose of the changes.
- Summarizes major additions/removals/updates.
- Highlights any bug fixes, features, or refactors.
- Uses bullet points and markdown formatting if helpful.
- Avoids unnecessary repetition of file names.

PR Description:
"""

    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that writes GitHub PR descriptions."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 500
    }

    response = requests.post(
        AZURE_API_ENDPOINT,
        headers=HEADERS,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print("Error from Azure OpenAI API:", response.status_code, response.text)
        return ""

# pr_description_gen.py
def generate_description_from_diff(diff_text):
    """Same logic, but takes diff as input instead of calling git."""
    print("🤖 Generating PR description using GPT-4o-mini...")
    description = generate_pr_description(diff_text)
    return description

