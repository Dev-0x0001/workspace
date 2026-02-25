from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass(kw_only=True)
class GitHubPR:
    """Represents a GitHub Pull Request"""

    number: int
    title: str
    body: str
    url: str
    state: str
    created_at: datetime
    updated_at: datetime
    merged_at: Optional[datetime] = None
    head: Dict[str, Any] = field(default_factory=dict)
    base: Dict[str, Any] = field(default_factory=dict)
    _raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
def from_json(cls, data: Dict[str, Any]) -> 'GitHubPR':
        return cls(
            number=data['number'],
            title=data['title'],
            body=data['body'],
            url=data['html_url'],
            state=data['state'],
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if 'updated_at' in data else datetime.now(),
            merged_at=datetime.fromisoformat(data['merged_at']) if 'merged_at' in data and data['merged_at'] else None,
            head=data.get('head', {}),
            base=data.get('base', {}),
            _raw=data.copy()
        )


@dataclass(kw_only=True)
class GitHubFile:
    """Represents a file in a GitHub PR"""

    filename: str
    status: str
    additions: int
    deletions: int
    changes: int
    blob_url: str
    raw_url: str

    @classmethod
def from_json(cls, data: Dict[str, Any]) -> 'GitHubFile':
        return cls(
            filename=data['filename'],
            status=data['status'],
            additions=data['additions'],
            deletions=data['deletions'],
            changes=data['changes'],
            blob_url=data['blob_url'],
            raw_url=data['raw_url']
        )


@dataclass(kw_only=True)
class GitHubAPIResponse:
    """Represents a response from GitHub API"""

    data: Dict[str, Any]
    status_code: int
    headers: Dict[str, Any] = field(default_factory=dict)
    
    @property
def json(self) -> Dict[str, Any]:
        return self.data


class GitHubClient:
    """Client for interacting with GitHub API"""

    def __init__(self, token: str, repo_owner: str, repo_name: str):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.session = self._create_session()

    def _create_session(self):
        """Create a session with GitHub API"""
        import requests
        session = requests.Session()
        session.headers.update({
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        })
        return session

    def _make_request(self, method: str, path: str, params: Dict[str, Any] = None, data: Dict[str, Any] = None):
        """Make a request to GitHub API"""
        url = f"{self.base_url}/{path.lstrip('/')}" if path.startswith('/') else f"{self.base_url}/{path}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            
            if response.headers['Content-Type'] == 'application/json':
                return GitHubAPIResponse(
                    data=response.json(),
                    status_code=response.status_code,
                    headers=response.headers
                )
            else:
                return GitHubAPIResponse(
                    data={'text': response.text},
                    status_code=response.status_code,
                    headers=response.headers
                )
        except requests.exceptions.RequestException as e:
            return GitHubAPIResponse(
                data={'error': str(e)},
                status_code=500,
                headers={}
            )

    def create_pull_request(
        self, title: str, body: str, head: str, base: str = 'main'
    ) -> GitHubAPIResponse:
        """Create a new pull request"""
        data = {
            'title': title,
            'body': body,
            'head': head,
            'base': base
        }
        
        return self._make_request('POST', '/pulls', data=data)

    def get_pull_request(self, pr_number: int) -> GitHubAPIResponse:
        """Get details of a pull request"""
        return self._make_request('GET', f'/pulls/{pr_number}')

    def list_pull_requests(
        self, state: str = 'all', per_page: int = 30
    ) -> GitHubAPIResponse:
        """List pull requests"""
        params = {'state': state, 'per_page': per_page}
        return self._make_request('GET', '/pulls', params=params)

    def create_or_update_file(
        self, path: str, content: str, message: str, branch: str = 'main'
    ) -> GitHubAPIResponse:
        """Create or update a file in the repository"""
        
        # First, get the file's current content to calculate SHA
        file_response = self._make_request('GET', f'/contents/{path}', params={'ref': branch})
        
        if file_response.status_code == 200:
            # File exists - update it
            sha = file_response.json()['sha']
            content = self._encode_content(content)
            
            data = {
                'message': message,
                'content': content,
                'sha': sha,
                'branch': branch
            }
        else:
            # File doesn't exist - create it
            data = {
                'message': message,
                'content': self._encode_content(content),
                'branch': branch
            }
        
        return self._make_request('PUT', f'/contents/{path}', data=data)

    def _encode_content(self, content: str) -> str:
        """Base64 encode content for GitHub API"""
        import base64
        return base64.b64encode(content.encode('utf-8')).decode('utf-8')


class GitHubFileManager:
    """Handles file operations on GitHub"""

    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client

    def create_file(self, path: str, content: str, message: str, branch: str = 'main') -> GitHubAPIResponse:
        """Create a new file in the repository"""
        return self.github_client.create_or_update_file(path, content, message, branch)

    def update_file(self, path: str, content: str, message: str, branch: str = 'main') -> GitHubAPIResponse:
        """Update an existing file in the repository"""
        return self.github_client.create_or_update_file(path, content, message, branch)

    def get_file_content(self, path: str, branch: str = 'main') -> Optional[str]:
        """Get the content of a file"""
        response = self.github_client._make_request('GET', f'/contents/{path}', params={'ref': branch})
        
        if response.status_code == 200:
            content = response.json()['content']
            return base64.b64decode(content).decode('utf-8')
        return None