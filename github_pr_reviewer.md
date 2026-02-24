# GitHub PR Reviewer

Handles pull request review operations for the workspace repository.

## Features
- Fetch PR details
- Create review comments
- Create/update files

## Usage
```python
if __name__ == '__main__':
 reviewer = GitHubPRReviewer('your-token')

 # Get PR details
 pr_details = reviewer.get_pr_details(123)

 # Create a review comment
 comment_result = reviewer.create_review_comment(
 pr_number=123,
 comment="This looks good",
 file_path='file.py',
 line=42
 )
```