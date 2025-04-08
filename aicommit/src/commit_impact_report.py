import os
import subprocess
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_API_ENDPOINT = (
    "https://shrutiaiinstance.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"
)

HEADERS = {
    "Content-Type": "application/json",
    "api-key": OPENAI_API_KEY
}

def get_commit_diff():
    """Get the full diff from the latest commit."""
    try:
        diff = subprocess.check_output(
            ["git", "show", "--no-color"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8")
        return diff.strip()
    except subprocess.CalledProcessError as e:
        print("❌ Error getting git diff:", e)
        return ""

def generate_impact_report(diff_text):
    """Call Azure OpenAI to generate impact area analysis report."""
    prompt = f"""
You're an expert code reviewer and software architect.

Given the following `git diff` from a backend project, perform an **Impact Area Analysis Report**. Be highly specific and professional.

Your report should include:
- **APIs Affected**: List impacted endpoints or controller functions (e.g., GET /users, PUT /product/:id).
- **Modules Changed**: Identify modules, services, DTOs, or helper files that were updated.
- **Reasoning**: For each impact, explain how the change could affect functionality, performance, or security.
- **Potential Risks**: Highlight anything that might break or needs careful testing.
- **Suggested Tests**: Recommend test cases that should be added or rerun.

Use clear markdown-style formatting.

Git Diff:
{diff_text}

Now provide the Impact Area Analysis Report:
"""

    payload = {
        "messages": [
            {"role": "system", "content": "You are a senior developer reviewing code changes."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 800
    }

    response = requests.post(
        AZURE_API_ENDPOINT,
        headers=HEADERS,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print("❌ Azure OpenAI API Error:", response.status_code, response.text)
        return ""

def commit_impact_report():
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY not set in .env")
        return

    print("📦 Fetching latest commit diff...")
    diff = get_commit_diff()
    if not diff:
        print("⚠️ No changes detected.")
        return

    print("🧠 Generating Impact Area Analysis Report...")
    report = generate_impact_report(diff)

    if report:
        print("\n--- 🧾 Impact Area Analysis Report ---\n")
        # print(report)
        
        os.makedirs(".github", exist_ok=True)
        with open(".github/IMPACT_REPORT.md", "w", encoding="utf-8") as f:
            f.write(report)
        
        print("\n💾 Impact report saved to `.github/IMPACT_REPORT.md`")
    else:
        print("❌ Failed to generate impact report.")

        """hellooo"""