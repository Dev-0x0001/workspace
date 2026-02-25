import json
import os
from datetime import datetime

class AgentState:
    """
    Represents the agent's current state and progress
    """

    def __init__(self, state_data=None):
        self.state = state_data or {}
        self.history = []
        self.memory = []
        self._last_id = 0

    def update(self, key, value):
        """Update a state variable"""
        self.state[key] = value
        self._last_id += 1
        return self._last_id

    def get(self, key, default=None):
        """Get a state variable"""
        return self.state.get(key, default)

    def add_history(self, action):
        """Add an action to the history"""
        self.history.append(action)

    def add_memory(self, memory):
        """Add a memory"""
        self.memory.append(memory)

    def to_dict(self):
        """Convert state to dictionary"""
        return {
            'state': self.state,
            'history': self.history,
            'memory': self.memory,
        }

    def from_dict(cls, data):
        """Create state from dictionary"""
        state = AgentState()
        state.state = data.get('state', {})
        state.history = data.get('history', [])
        state.memory = data.get('memory', [])
        return state


# Example usage
if __name__ == "__main__":
    # Create initial state
    state = AgentState({
        'now_doing': 'understand_my_current_state',
        'doing_next': 'plan_next_steps',
        'permanent_goal': None,
        'current_goal': 'understand_my_current_state',
        'done_history': [],
        'memories': [],
    })

    # Demonstrate updates
    print(f"Initial state: {json.dumps(state.to_dict(), indent=2)}")

    # Update state
    state.update('now_doing', 'analyze_state_variables')
    state.update('current_goal', 'analyze_state_variables')
    state.add_history('understand_my_current_state')
    state.add_memory('reviewed_initial_state')

    print(f"\nState after updates:")
    print(json.dumps(state.to_dict(), indent=2))

    # Save state to file
    with open('agent_state.json', 'w') as f:
        json.dump(state.to_dict(), f, indent=2)

    print(f"\nState saved to agent_state.json")