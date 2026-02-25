import asyncio
import json
from datetime import datetime

from .agent_state import AgentState

class StateManager:
    """
    Manages the agent's state persistence and retrieval
    """

    def __init__(self, storage_path='agent_state.json', max_history=100, max_memory=50):
        self.storage_path = storage_path
        self.max_history = max_history
        self.max_memory = max_memory
        self._state = AgentState()
        self._dirty = False

    async def load_state(self):
        """Load state from persistent storage"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                self._state = AgentState.from_dict(data)
                self._dirty = False
                return True
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {self.storage_path}",
                      "Creating new state...")
                self._state = AgentState()
                self._dirty = False
                return False
        return False

    async def save_state(self):
        """Save state to persistent storage"""\n        if self._dirty:
            try:
                with open(self.storage_path, 'w') as f:
                    json.dump(self._state.to_dict(), f, indent=2)
                self._dirty = False
                return True
            except Exception as e:
                print(f"Error saving state: {e}")
                return False
        return False

    def get_state(self):
        """Get the current state"""
        return self._state

    def update_state(self, key, value):
        """Update a state variable and mark state as dirty"""
        self._state.update(key, value)
        self._dirty = True
        return self._state.get(key)

    def add_history(self, action):
        """Add an action to history and mark state as dirty"""
        self._state.add_history(action)
        self._dirty = True

    def add_memory(self, memory):
        """Add a memory and mark state as dirty"""
        self._state.add_memory(memory)
        self._dirty = True

    def prune(self):
        """Prune excess history and memory"""
        if len(self._state.history) > self.max_history:
            self._state.history = self._state.history[-self.max_history:]}
        if len(self._state.memory) > self.max_memory:
            self._state.memory = self._state.memory[-self.max_memory:]


# Example usage
if __name__ == "__main__":
    async def main():
        manager = StateManager()
        
        # Load or create new state
        print("Loading state...")
        loaded = await manager.load_state()
        if not loaded:
            print("Creating new state...")
            manager.update_state('now_doing', 'initial_state')
            manager.update_state('current_goal', 'initial_state')
            manager.add_memory('state_manager_initialized')
        
        # Demonstrate state operations
        print(f"
Current state:")
        print(json.dumps(manager.get_state().to_dict(), indent=2))
        
        # Update state
        manager.update_state('now_doing', 'performing_actions')
        manager.update_state('current_goal', 'complete_tasks')
        manager.add_history('action_1')
        manager.add_history('action_2')
        manager.add_memory('completed_actions')
        
        print(f"
State after updates:")
        print(json.dumps(manager.get_state().to_dict(), indent=2))
        
        # Save state
        print(f"
Saving state...")
        saved = await manager.save_state()
        if saved:
            print("State saved successfully!")
        else:
            print("Failed to save state")

    asyncio.run(main())