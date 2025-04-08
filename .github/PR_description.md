### 📝 Description
In this PR, I added new search algorithms and improved the impact reporting functionality. The changes enhance our codebase by introducing efficient search methods and refining how we generate impact reports for commits. The following areas were impacted:

### 📁 Files Changed
- **`.github/IMPACT_REPORT.md`**: Added documentation for the impact report format and usage.
- **`.github/PR_description.md`**: Introduced a template for pull request descriptions to standardize contributions.
- **`aicommit/src/commit_impact_report.py`**: Modified the impact report logic to accommodate new features and ensure accurate reporting.
- **`project/binary_search.py`**: Implemented the binary search algorithm to improve search efficiency.
- **`project/linear_search.py`**: Added the linear search algorithm as a straightforward alternative for educational purposes.

### 🛠️ Impact Areas
The changes primarily impact the search functionalities within the `project` module and the commit impact reporting in the `aicommit` module. The new search algorithms provide developers with more efficient options for data retrieval, while the updates to the impact report enhance our ability to track changes and understand the effects of commits on the project.

### ✅ Summary of Changes
- **Added** the binary search algorithm to improve search efficiency in sorted datasets.
- **Introduced** a linear search algorithm for basic use cases and educational purposes.
- **Updated** the impact report generation logic to reflect the new search functionalities and improve clarity in reporting. 
- **Created** documentation files to guide users on the usage of the impact report and PR description templates.