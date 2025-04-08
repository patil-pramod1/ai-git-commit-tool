import subprocess
import os
from dotenv import load_dotenv
from .pr_description_gen import generate_description
from .utils import generate_commit_messages, get_diff

def main():
    """
    Main function to generate and commit a git commit message.
    """
    # Load environment variables
    load_dotenv()
    
    # Get the git diff
    diff = get_diff(diff_per_file=False)
    
    if not diff:
        print("No staged changes found. Make sure there are changes and run `git add .`")
        return

    # Get API key from environment or use the one you provided
    # For security, it's better to use environment variables rather than hardcoding
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    commit_language = "en"

    try:
        choices = generate_commit_messages(OPENAI_API_KEY, diff, commit_language)
        
        if len(choices) == 0:
            print("No commit message generated.")
            return

        # Display the choices to the user
        print("\nGenerated Commit Messages:")
        for idx, msg in enumerate(choices, 1):
            print(f"{idx}. {msg}")

        # Ask the user to choose a commit message
        try:
            commit_choice = int(input("\nSelect a commit message (enter number): ")) - 1
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        if commit_choice < 0 or commit_choice >= len(choices):
            print("Invalid choice")
            return

        selected_message = choices[commit_choice]
        print(f"\nSelected Commit Message:\n{selected_message}")

        # Confirm the commit
        confirmation = input("\nWould you like to use this commit message? (y/n): ").lower()
        if confirmation == 'y':
            # generate_description()
            subprocess.run(["git", "commit", "-m", selected_message])
            print("Changes committed!")
            print('Start generating PR description...')
            generate_description()
            print('PR description generated successfully!')


        else:
            print("Commit message was not used.")
    except Exception as e:
        print(f"Error: {e}")