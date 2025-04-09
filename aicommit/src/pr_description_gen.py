import os
import subprocess
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file (e.g., API keys)
load_dotenv()

# --- CONFIG ---
# Retrieve OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Azure OpenAI API endpoint for the GPT-4o-mini chat completion deployment
AZURE_API_ENDPOINT = (
    "https://shrutiaiinstance.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"
)

# Headers for the API request including content type and API key for authentication
HEADERS = {
    "Content-Type": "application/json",
    "api-key": OPENAI_API_KEY
}

def get_branch_diff_against_master():
    """Compare current branch against master and return the diff."""
    try:
        # Run git diff to get the list of file changes compared to origin/master
        diff = subprocess.check_output(
            ["git", "diff", "origin/master...HEAD", "--name-status", "--no-color"]
        ).decode("utf-8")
        return diff.strip()
    except subprocess.CalledProcessError as e:
        # Log error if git diff command fails
        print("Error fetching branch diff against master:", e)
        return ""

def generate_pr_description(diff_text):
    """Generate structured PR description using Azure OpenAI."""
    # Create a prompt with instructions for the AI to generate a PR description
    prompt = f"""
You are an expert AI assistant that writes professional and structured GitHub Pull Request descriptions.

You are comparing the current branch against the `master` branch. Based on the following git diff output, generate a PR description that:

- Clearly explains what was changed and why.
- Mentions **files changed**.
- Highlights **impacted areas or modules**.
- Groups changes by purpose (e.g., bug fix, refactor, optimization).
- Uses markdown formatting (e.g., bullet points, bold headers).
- Follows the below structure:

### 📝 Description
In this PR, I [describe the main issue addressed or feature added]. The following areas were impacted:

### 📁 Files Changed
List the major files or modules that were changed and explain briefly why.

### 🛠️ Impact Areas
Explain which functionalities, APIs, or modules were affected by the changes and why.

### ✅ Summary of Changes
- [Bullet 1: Describe a fix, rename, or optimization]
- [Bullet 2: Summarize a file refactor, logic update, or cleanup]
- [Bullet 3: Any performance or readability improvements]

Git Diff to Analyze:

{diff_text}


Now write the PR description following the structure above.
"""

    # Build the payload for the API call including the messaging structure required by the service
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

    # Send the payload to the Azure OpenAI endpoint to generate the PR description
    response = requests.post(
        AZURE_API_ENDPOINT,
        headers=HEADERS,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        # Return the generated PR description if the request is successful
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        # Log any errors returned by the API
        print("Error from Azure OpenAI API:", response.status_code, response.text)
        return ""

def generate_description():
    # Ensure that the API key is available in the environment
    if not OPENAI_API_KEY:
        print("❌ AZURE_API_KEY not found in environment or .env file.")
        exit(1)

    print("🔍 Fetching latest commit changes...")
    # Retrieve diff of the current branch against master
    diff = get_branch_diff_against_master()

    if not diff:
        # Exit if no changes are detected in the diff
        print("⚠️ No changes found in the latest commit.")
        exit(0)

    print("🤖 Generating PR description using GPT-4o-mini...")
    # Generate a PR description from the diff
    description = generate_pr_description(diff)
    # Uncomment the following lines to print the generated description on the console:
    # print("\n--- 📝 Generated PR Description ---\n")
    # print(description)

    # Ensure the .github directory exists or create it if necessary
    os.makedirs(".github", exist_ok=True)
    
    # Save the generated PR description to a markdown file
    with open(".github/PR_description.md", "w", encoding="utf-8") as f:
        f.write(description)

    print("\n💾 PR description saved to `.github/PR_DESCRIPTION.md`")
