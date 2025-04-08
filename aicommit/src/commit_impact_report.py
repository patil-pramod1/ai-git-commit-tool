import os
import subprocess
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from openpyxl import Workbook, load_workbook
from io import BytesIO

# Load environment variables
load_dotenv()

# Azure OpenAI Setup
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_API_ENDPOINT = "https://shrutiaiinstance.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"
HEADERS = {
    "Content-Type": "application/json",
    "api-key": OPENAI_API_KEY
}

# Microsoft Graph Auth Setup
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
EXCEL_FILE_PATH_ONEDRIVE = "/drive/root:/PR_Report.xlsx"  # Change path as needed


def get_access_token():
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    payload = {
        'client_id': CLIENT_ID,
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]


def download_excel_file(access_token):
    url = f"https://graph.microsoft.com/v1.0{EXCEL_FILE_PATH_ONEDRIVE}:/content"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return BytesIO(response.content) if response.status_code == 200 else None


def upload_excel_file(access_token, file_content):
    url = f"https://graph.microsoft.com/v1.0{EXCEL_FILE_PATH_ONEDRIVE}:/content"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }
    response = requests.put(url, headers=headers, data=file_content)
    if response.status_code in [200, 201]:
        print("✅ Excel file updated on OneDrive.")
    else:
        print(f"❌ Failed to upload Excel file: {response.status_code}")
        print(response.text)


def append_to_excel_onedrive(date, username, commit_message, impact_summary):
    # Original OneDrive implementation (to be implemented later):
    # access_token = get_access_token()
    # file_stream = download_excel_file(access_token)
    #
    # if file_stream:
    #     workbook = load_workbook(file_stream)
    # else:
    #     workbook = Workbook()
    #     workbook.active.append(["Date", "GitHub Username", "Commit Message", "Impacted Modules Summary"])
    #
    # sheet = workbook.active
    # sheet.append([date, username, commit_message, impact_summary])
    #
    # output_stream = BytesIO()
    # workbook.save(output_stream)
    # upload_excel_file(access_token, output_stream.getvalue())
    
    # Local Excel file implementation in the .github folder:
    local_excel_path = ".github/PR_Report.csv"
    if os.path.exists(local_excel_path):
        workbook = load_workbook(local_excel_path)
    else:
        workbook = Workbook()
        workbook.active.append(["Date", "GitHub Username", "Commit Message", "Impacted Modules Summary"])
    
    sheet = workbook.active
    sheet.append([date, username, commit_message, impact_summary])
    workbook.save(local_excel_path)


def get_commit_diff():
    try:
        diff = subprocess.check_output(["git", "diff", "master..HEAD", "--no-color"], stderr=subprocess.DEVNULL)
        return diff.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        print("❌ Error getting git diff:", e)
        return ""


def generate_impact_report(diff_text):
    prompt = f"""
        You're an expert code reviewer and software architect.

        Given the following git diff from a project that may include both backend and frontend code, perform an Impact Area Analysis Report. Include:

        - **APIs Affected**
        - **Modules Changed (Backend)**
        - **Frontend Changes**
        - **Reasoning**

        Git Diff:
        {diff_text}
        """
    payload = {
        "messages": [
            {"role": "system", "content": "You are a senior developer reviewing code changes."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 800
    }
    response = requests.post(AZURE_API_ENDPOINT, headers=HEADERS, data=json.dumps(payload))
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

        # Append to Excel on OneDrive
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        username = get_git_username()
        commit_message = get_commit_message()
        summary = report[:1000] + "..." if len(report) > 1000 else report
        append_to_excel_onedrive(date, username, commit_message, summary)
    else:
        print("❌ Failed to generate impact report.")