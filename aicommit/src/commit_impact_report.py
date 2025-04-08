import os
import subprocess
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
from openpyxl import Workbook, load_workbook

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

# 📁 Path to Excel file (store this in OneDrive if needed)
EXCEL_FILE_PATH = os.path.expanduser("https://adaptnxt-my.sharepoint.com/:x:/r/personal/logith_adaptnxt_com/_layouts/15/Doc2.aspx?action=editNew&sourcedoc=%7B5b6c874a-d93e-4a0b-87e0-103cd9d6f7c8%7D&wdOrigin=TEAMS-MAGLEV.teamsSdk_ns.rwc&wdExp=TEAMS-TREATMENT&wdhostclicktime=1744110592367&web=1")  # Update path if needed


def get_commit_diff():
    """Get the diff by comparing the master branch with the current branch."""
    try:
        diff = subprocess.check_output(
            ["git", "diff", "master..HEAD", "--no-color"],
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

        Given the following git diff from a project that may include both backend and frontend code (such as React or Angular projects), perform an Impact Area Analysis Report. Provide detailed analysis in a bullet point format, ensuring that each module lists its impacts as clear point-by-point statements. Only include points that are critical.

        Your report should include:
        - **APIs Affected**: 
          - If any API changes are detected, list the impacted endpoints or controller functions (e.g., GET /users, PUT /product/:id) using bullet points.
        - **Modules Changed (Backend)**: 
          - Identify updated modules, services, DTOs, or helper files on the backend. For each, include the important changes as individual bullet points.
        - **Frontend Changes**:
          - For projects using frontend frameworks like React or Angular, identify changes in components, views, state management, or UI logic. List these changes using bullet points.
        - **Reasoning**: 
          - For each impacted module, API, or frontend component, provide concise bullet points explaining how the change could affect functionality, performance, or security.

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


def get_commit_message():
    try:
        return subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return "N/A"


def get_git_username():
    try:
        return subprocess.check_output(["git", "config", "user.name"]).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return "N/A"


def append_to_excel(date, username, commit_message, impact_summary):
    file_path = EXCEL_FILE_PATH

    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
    except FileNotFoundError:
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Date", "GitHub Username", "Commit Message", "Impacted Modules Summary"])

    sheet.append([date, username, commit_message, impact_summary])
    workbook.save(file_path)
    print(f"📊 Appended summary to `{file_path}`")


def impact_report():
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

        os.makedirs(".github", exist_ok=True)
        with open(".github/IMPACT_REPORT.md", "w", encoding="utf-8") as f:
            f.write(report)

        print("💾 Impact report saved to `.github/IMPACT_REPORT.md`")

        # ✨ Append metadata to Excel
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        username = get_git_username()
        commit_message = get_commit_message()
        summary = report[:1000] + "..." if len(report) > 1000 else report

        append_to_excel(date, username, commit_message, summary)
    else:
        print("❌ Failed to generate impact report.")