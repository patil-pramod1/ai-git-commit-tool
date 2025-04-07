import subprocess
import openai
from openai import AzureOpenAI

def generate_commit_messages(
    api_key: str, prompt: str, language: str = "english", num_messages: int = 5
) -> list:
    try:
        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2025-01-01-preview",
            azure_endpoint="https://shrutiaiinstance.openai.azure.com"
        )
        
        # Format prompt
        prompt = f"What follows '-------' is a git diff for a potential commit. Reply with an appropriate git commit message (a Git commit message should be concise but also try to describe the important changes in the commit) and don't include any other text but the message in your response. ------- {prompt}, language={language}"

        # Make the API call using the appropriate Azure OpenAI endpoint
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # This is your deployment name
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates git commit messages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            n=num_messages,
            temperature=0.7,
        )

        # Extract and return the commit messages from the response
        messages = [choice.message.content.strip().replace("\n", "") for choice in response.choices]
        return messages
    except Exception as e:
        error_message = f"Azure OpenAI API Error: {e}"
        print(error_message)
        raise e

def get_diff(diff_per_file: bool) -> str:
    if diff_per_file:
        diff = subprocess.check_output(
            "git diff --cached --name-only",
            shell=True,
            stderr=subprocess.STDOUT,
        ).decode("utf-8")

        files_changed = diff.split("\n")[:-1]
        diff_string = ""
        for file in files_changed:
            diff_string += subprocess.check_output(
                f"git diff --cached -- {file}",
                shell=True,
                stderr=subprocess.STDOUT,
            ).decode("utf-8")
    else:
        diff_string = subprocess.check_output(
            "git diff --cached .",
            shell=True,
            stderr=subprocess.STDOUT,
        ).decode("utf-8")

    return diff_string