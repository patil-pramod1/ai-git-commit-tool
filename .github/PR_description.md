### 📝 Description
In this PR, I have made several updates to enhance the functionality of the AI Commit tool, specifically by adding a new module for generating commit impact reports. This addresses the need for better insights into changes made during commits, improving the developer's ability to track and understand modifications.

### 📁 Files Changed
- **.github/update_pr_description.py**: Modified to include the new module's functionality and ensure that the PR description is updated accordingly.
- **aicommit/src/aicommit.py**: Updated to integrate the new commit impact reporting features, allowing for improved analysis of changes.
- **aicommit/src/commit_impact_report.py**: A new file that implements the logic for generating reports on the impact of recent commits.

### 🛠️ Impact Areas
The following functionalities and modules were affected by the changes:
- **AI Commit Tool**: The main tool has been enhanced with reporting capabilities, which will now provide insights into the impact of each commit, facilitating better decision-making during the development process.
- **PR Automation**: The integration with the update PR description script ensures that any relevant information is automatically included in PRs, streamlining the workflow for developers.

### ✅ Summary of Changes
- **Added** a new module `commit_impact_report.py` to generate reports detailing the impact of commits.
- **Updated** the `aicommit.py` file to integrate the new reporting features, improving the overall functionality of the AI Commit tool.
- **Modified** the `.github/update_pr_description.py` script to incorporate the new reporting capabilities, enhancing the automation of PR descriptions.