import subprocess
import openai
from .commit_impact_report import commit_impact_report,generate_impact_report
from .utils import generate_commit_messages, get_diff
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def check_for_merge_conflicts():
    """
    Check for merge conflicts by comparing staged changes with the remote branch.
    Returns:
        bool: True if conflicts exist, False otherwise.
        list: List of files with conflicts if any.
    """
    print("Checking for merge conflicts...")

    try:
        # Fetch the latest changes from the remote repository
        subprocess.run(["git", "fetch"], check=True)
        
        # Check for conflicts using `git diff --name-only --diff-filter=U`
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=U"],
            capture_output=True, text=True, check=True
        )

        # Split the output by lines, ignoring empty ones
        conflicting_files = [file.strip() for file in result.stdout.split("\n") if file.strip()]

        if conflicting_files:
            print("Merge conflicts detected in the following files:")
            for file in conflicting_files:
                print(f"- {file}")
            return True, conflicting_files  # Conflicts found, return files involved
        else:
            print("No conflicts detected.")
            return False, []  # No conflicts
    except subprocess.CalledProcessError as e:
        print(f"Error during conflict check: {e}")
        return False, []  # In case of error, assume no conflicts

def main():
    """
    Main function to generate and commit a git commit message.
    """
    # Check for conflicts and pull the latest changes if necessary
    conflicts, conflicting_files = check_for_merge_conflicts()
    
    if conflicts:
        print("Please resolve the conflicts before proceeding with the commit.")
        # Optionally, you could also prompt the user here to resolve conflicts manually
        return  # Exit if conflicts are detected
    
    # Get the git diff
    diff = get_diff(diff_per_file=False)
    
    if not diff:
        print("No staged changes found. Make sure there are changes and run `git add .`")
        return

    # Set up the API key and generate commit messages
    commit_language = "en"

    choices = generate_commit_messages(OPENAI_KEY, diff, commit_language)

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
        subprocess.run(["git", "commit", "-m", selected_message])
        print("Changes committed!")
        commit_impact_report()
        generate_impact_report(diff)
       
    else:
        print("Commit message was not used.")
