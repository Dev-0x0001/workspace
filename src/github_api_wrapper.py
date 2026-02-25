# GitHub API Wrapper

A simple wrapper for interacting with the GitHub API.

## Features
- Create repositories
- Manage issues and pull requests
- View commit history
- Deploy workflows

## Installation
```bash
pip install github-api-wrapper
```

## Usage
```python
from github_api import GitHubClient

client = GitHubClient(token='your-token')

# Create a new repository
client.create_repo('username', 'repo-name')

# Create a pull request
client.create_pull_request(
    'username',
    'repo-name',
    'main',
    'feature-branch',
    'PR Title',
    'PR Body'
)
