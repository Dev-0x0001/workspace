#!/usr/bin/env python3

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

import requests
from requests.auth import HTTPBasicAuth

# Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
if not GITHUB_TOKEN:
sys.exit("Error: GITHUB_TOKEN environment variable not set")

# Set up logging
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"[INFO] Script started at {current_time}")

class GitHubPRReviewer:
 """Handles GitHub pull request review operations"""

 def __init__(self, token: str):
 self.token = token
 self.session = self._create_session()

 def _create_session(self) -> requests.Session:
 """Create a requests session with GitHub authentication"""
 session = requests.Session()
 session.auth = HTTPBasicAuth('Dev-0x0001', self.token)
 session.headers.update({'Accept': 'application/vnd.github.v3+json'})
 return session

 def get_pr_details(self, pr_number: int) -> Dict[str, Any]:
 """Retrieve details for a specific pull request"""
 url = f'https://api.github.com/repos/Dev-0x0001/workspace/pulls/{pr_number}'
 
 try:
 response = self.session.get(url)
 response.raise_for_status()
 return response.json()
 except requests.exceptions.HTTPError as e:
 if response.status_code == 404:
 raise ValueError(f'PR #{pr_number} not found')
 raise

 def create_review_comment(self,
 pr_number: int,
 comment: str,
 file_path: str,
 line: int,
 position: Optional[int] = None,
 start_line: Optional[int] = None,
):
 """Create a comment on a pull request diff"""
 url = f'https://api.github.com/repos/Dev-0x0001/workspace/pulls/{pr_number}/comments'

 payload = {
 'body': comment,
 'path': file_path,
 'line': line,
 }
 if position is not None:
 payload['position'] = position
 if start_line is not None:
 payload['start_line'] = start_line

 try:
 response = self.session.post(url, json=payload)
 response.raise_for_status()
 return response.json()
 except requests.exceptions.RequestException as e:
 print(f'Error creating review comment: {e}')
 return None

 def create_or_update_file(self,
 file_path: str,
 content: str,
 commit_message: str,
 branch: str = 'main',
):
 """Create or update a file in the repository"""
 
 # Check if file exists
 file_url = f'https://api.github.com/repos/Dev-0x0001/workspace/contents/{file_path}'
 response = self.session.get(file_url)

 if response.status_code == 200:
 # File exists - update it
 file_info = response.json()
 sha = file_info['sha']

 payload = {
 'message': commit_message,
 'content': content,
 'sha': sha,
 }
 
 else:
 # File doesn't exist - create it
 payload = {
 'message': commit_message,
 'content': content,
 }

 url = f'https://api.github.com/repos/Dev-0x0001/workspace/contents/{file_path}'
 try:
 response = self.session.put(
 url,
 json=payload,
 headers={'Accept': 'application/vnd.github.v3+json'},
 )
 response.raise_for_status()
 return response.json()
 except requests.exceptions.RequestException as e:
 print(f'Error creating/updating file: {e}')
 return None

if __name__ == '__main__':
 # Main execution
 reviewer = GitHubPRReviewer(GITHUB_TOKEN)

 # Example usage
 PR_NUMBER = 123
 COMMENT_TEXT = "I'm analyzing my current state and planning my next steps"
 FILE_PATH = 'state_analysis.py'
 LINE_NUMBER = 34

 try:
 # Step 1: Verify PR exists
 pr_details = reviewer.get_pr_details(PR_NUMBER)
 print(f"[INFO] PR #{PR_NUMBER} details: {pr_details}")

 # Step 2: Add comment to PR
 comment_result = reviewer.create_review_comment(
 pr_number=PR_NUMBER,
 comment=COMMENT_TEXT,
 file_path=FILE_PATH,
 line=LINE_NUMBER,
 start_line=29
 )

 if comment_result:
 print(f"[SUCCESS] Comment added: {comment_result}")
 else:
 print("[ERROR] Failed to add comment")

 except ValueError as ve:
 print(f"[ERROR] {ve}")

 except Exception as e:
 print(f"[ERROR] Unexpected error: {e}")