# update_pr_description.py
import os
import requests
import subprocess
from pr_description_gen import generate_description_from_diff

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")
REPO = os.getenv("GITHUB_REPOSITORY")  # user/repo

def get_pr_diff(pr_number, repo):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None

def update_pr_description(pr_number, repo, new_description):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "body": new_description
    }
    response = requests.patch(url, headers=headers, json=payload)
    return response.status_code == 200

if __name__ == "__main__":
    diff = get_pr_diff(PR_NUMBER, REPO)
    if diff:
        description = generate_description_from_diff(diff)
        success = update_pr_description(PR_NUMBER, REPO, description)
        if success:
            print("✅ PR description updated successfully.")
        else:
            print("❌ Failed to update PR description.")
            print("🔍 Debug Info:")
            print("PR_NUMBER:", PR_NUMBER)
            print("REPO:", REPO)
            print("DESCRIPTION:", description)
    else:
        print("❌ Could not retrieve PR diff.")
