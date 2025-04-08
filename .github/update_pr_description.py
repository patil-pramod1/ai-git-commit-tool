# update_pr_description.py
import os
import requests
from pr_description_gen import get_latest_commit_diff

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

    if response.status_code != 200:
        print("❌ GitHub API PATCH failed:")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

    return response.status_code == 200

if __name__ == "__main__":
    if not GITHUB_TOKEN or not PR_NUMBER or not REPO:
        print("❌ Missing one of GITHUB_TOKEN, PR_NUMBER, or GITHUB_REPOSITORY.")
        print("GITHUB_TOKEN:", bool(GITHUB_TOKEN))
        print("PR_NUMBER:", PR_NUMBER)
        print("GITHUB_REPOSITORY:", REPO)
        exit(1)

    diff = get_pr_diff(PR_NUMBER, REPO)
    if diff:
        description = get_latest_commit_diff(diff)

        if not description.strip():
            print("❌ Generated description is empty.")
            exit(1)

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
