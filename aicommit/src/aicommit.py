import subprocess
from .commit_impact_report import impact_report
from .pr_description_gen import generate_description
from .utils import generate_commit_messages, get_diff
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
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
        # Fetch the latest changes from the remote repository.
        subprocess.run(["git", "fetch"], check=True)
        
        # Get a list of files with merge conflicts via git diff.
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=U"],
            capture_output=True, text=True, check=True
        )

        # Process the output by splitting lines and remove empties
        conflicting_files = [file.strip() for file in result.stdout.split("\n") if file.strip()]

        if conflicting_files:
            # If there are conflicts, display them to the user.
            print("Merge conflicts detected in the following files:")
            for file in conflicting_files:
                print(f"- {file}")
            
            # Auto resolve conflicts by pulling the latest changes.
            print("\nAttempting to resolve conflicts by pulling the latest changes...")
            subprocess.run(["git", "pull", "origin", "master"], check=True)
            print("Merge conflicts resolved. Proceeding with commit generation.")
            
            return True, conflicting_files  # Return conflict status along with files involved.
        else:
            print("No conflicts detected.")
            return False, []  # No conflicts found.
    except subprocess.CalledProcessError as e:
        # If any subprocess command fails, log the error.
        print(f"Error during conflict check: {e}")
        return False, []  # In case of error, assume no conflicts.


def main():
    """
    Main function to generate and commit a git commit message.
    """
    # Check for conflicts and attempt to resolve if necessary.
    conflicts, conflicting_files = check_for_merge_conflicts()
    
    if conflicts:
        # If conflicts still exist after auto-resolving, exit the function.
        print("Please resolve the conflicts before proceeding with the commit.")
        return
    
    # Retrieve the git diff (all staged changes)
    diff = get_diff(diff_per_file=False)
    
    if not diff:
        # Ensure there is a diff. If not, instruct the user to stage changes.
        print("No staged changes found. Make sure there are changes and run `git add .`")
        return

    # Define the commit language (currently set to English)
    commit_language = "en"

    # Generate commit message suggestions using the provided OpenAI API key.
    choices = generate_commit_messages(OPENAI_KEY, diff, commit_language)

    if len(choices) == 0:
        # If no commit messages were generated, notify the user.
        print("No commit message generated.")
        return

    # Display the generated commit messages
    print("\nGenerated Commit Messages:")
    for idx, msg in enumerate(choices, 1):
        print(f"{idx}. {msg}")

    # Get the user's choice for the commit message.
    try:
        commit_choice = int(input("\nSelect a commit message (enter number): ")) - 1
    except ValueError:
        # Handle non-integer input from the user.
        print("Invalid input. Please enter a valid number.")
        return

    if commit_choice < 0 or commit_choice >= len(choices):
        # Validate the selected choice for range.
        print("Invalid choice")
        return

    # Retrieve the selected commit message based on user input.
    selected_message = choices[commit_choice]
    print(f"\nSelected Commit Message:\n{selected_message}")

    # Ask the user for confirmation to use the selected commit message.
    confirmation = input("\nWould you like to use this commit message? (y/n): ").lower()
    if confirmation == 'y':
        # Commit changes using the selected commit message.
        subprocess.run(["git", "commit", "-m", selected_message])
        print("Changes committed!")
        print('---------------------------------------------------------------------')
        print("Generating PR description and impact report...")
        # Generate the PR description.
        generate_description()
        # Generate the impact report.
        impact_report()

    else:
        # If the user cancels, print a cancellation message.
        print("Commit message was not used.")
