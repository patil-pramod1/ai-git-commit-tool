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

def get_branch_diff_against_master():
    """Compare current branch against master and return the diff."""
    try:
        diff = subprocess.check_output(
            ["git", "diff", "origin/master...HEAD", "--name-status", "--no-color"]
        ).decode("utf-8")
        return diff.strip()
    except subprocess.CalledProcessError as e:
        print("Error fetching branch diff against master:", e)
        return ""


def generate_pr_description(diff_text):
    """Generate structured PR description using Azure OpenAI."""
    prompt = f"""
    You are an expert AI assistant that writes professional and structured GitHub Pull Request descriptions.

    Analyze the following git diff between the current branch and the master branch. Generate a PR description that:
    - Provides a clear explanation of the changes and their purpose.
    - In the "Files Changed" section, only list the file names.
    - In the "Impact Areas" section, mention the affected modules or functionalities in exactly 10-20 words.
    - In the "Summary of Changes" section, include properly formatted bullet points explaining the fixes or improvements.

    Follow this structure exactly:

    ### 📝 Description
    Provide a precise explanation of the main issue addressed or feature implemented.

    ### 📁 Files Changed
    List only the file names that were changed.

    ### 🛠️ Impact Areas
    Describe the impacted areas in exactly 10-20 words.

    ### ✅ Summary of Changes
    - [Bullet 1: Provide a clear and concise description]
    - [Bullet 2: Summarize additional improvements]
    - [Bullet 3: Mention any performance or readability enhancements]

    Analyze the git diff below:

    {diff_text}

    Now generate the PR description following the instructions above.
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

def generate_description():
    if not OPENAI_API_KEY:
        print("❌ AZURE_API_KEY not found in environment or .env file.")
        exit(1)

    print("🔍 Fetching latest commit changes...")
    diff = get_branch_diff_against_master()

    if not diff:
        print("⚠️ No changes found in the latest commit.")
        exit(0)

    print("🤖 Generating PR description using GPT-4o-mini...")
    description = generate_pr_description(diff)
    # print("\n--- 📝 Generated PR Description ---\n")
    # print(description)

    # ✅ Save to .github/PR_description.md
    os.makedirs(".github", exist_ok=True)
    with open(".github/PR_description.md", "w", encoding="utf-8") as f:
        f.write(description)

    print("\n💾 PR description saved to `.github/PR_DESCRIPTION.md`")

