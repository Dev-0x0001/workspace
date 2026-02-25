import datetime
import json
import logging
import os
from typing import Dict, List, Optional

import requests

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

github_token = os.getenv('GITHUB_TOKEN')

class AgentState:
    """
    Tracks the autonomous AI agent's state and progress.
    """

    def __init__(self, state_file: str = 'workspace/agent_state.json'):
        self.state_file = state_file
        self.state: Dict = self.load_state()

    def load_state(self) -> Dict:
        """
        Loads the agent's state from disk or initializes it if missing.
        """
        
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        
        return {
            'now_doing': 'none',
            'doing_next': 'none',
            'permanent_goal': 'none',
            'goal': 'understand_my_current_state',
            'done_history': [],
            'memories': [],
            'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    def save_state(self) -> None:
        """
        Saves the agent's state to disk.
        """
        
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
        
        logger.info(f'Saved agent state to {self.state_file}')

    def update_state(
        self,
        now_doing: Optional[str] = None,
        doing_next: Optional[str] = None,
        permanent_goal: Optional[str] = None,
        goal: Optional[str] = None,
        done_history: Optional[List[str]] = None,
        memories: Optional[List[str]] = None,
    ) -> Dict:
        """
        Updates the agent's state with new information.
        """
        
        updates = {
            'now_doing': now_doing,
            'doing_next': doing_next,
            'permanent_goal': permanent_goal,
            'goal': goal,
            'done_history': done_history,
            'memories': memories,
        }
        
        for key, value in updates.items():
            if value is not None:
                self.state[key] = value
        
        self.state['timestamp'] = datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()
        
        self.save_state()
        
        return self.state

    def get_state(self) -> Dict:
        """
        Returns the current agent state.
        """
        return self.state

    def log_state(self, message: str = '') -> None:
        """
        Logs the current state with an optional message.
        """
        
        state_str = json.dumps(self.state, indent=2)
        
        if message:
            logger.info(f'{message}
{state_str}')
        else:
            logger.info(f'Current agent state:
{state_str}')

    def _github_api_request(
        self,
        method: str,
        path: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict:
        """
        Helper for making GitHub API requests.
        """
        
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        if method.lower() == 'get':
            response = requests.get(
                f'https://api.github.com/{path}',
                headers=headers,
                params=params
            )
        elif method.lower() == 'post':
            response = requests.post(
                f'https://api.github.com/{path}',
                headers=headers,
                json=data,
                params=params
            )
        elif method.lower() == 'patch':
            response = requests.patch(
                f'https://api.github.com/{path}',
                headers=headers,
                json=data,
                params=params
            )
        else:
            raise ValueError(f'Unsupported method: {method}')
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 201:
            return response.json()
        elif response.status_code == 204:
            return {}
        else:
            error_msg = f'GitHub API error ({response.status_code}): {response.text()}'
            logger.error(error_msg)
            raise Exception(error_msg)

    def create_pull_request(
        self,
        title: str,
        body: str,
        branch: str,
        files: List[Dict[str, str]]
    ) -> Dict:
        """
        Creates a new pull request with specified changes.
        """
        
        # First, create the new branch if it doesn't exist
        self._github_api_request(
            'POST',
            'repos/Dev-0x0001/workspace/git/refs',
            {'ref': branch, 'sha': self.state['head_sha']}
        )
        
        # Create files
        for file in files:
            self._github_api_request(
                'PUT',
                f'repos/Dev-0x0001/workspace/contents/{file[