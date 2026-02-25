import json
from typing import List, Dict, Any
from datetime import datetime

from .agent_state import AgentState
from .state_manager import StateManager

class StateHistory:
    """
    Tracks the agent's state changes over time
    """

    def __init__(self, max_entries: int = 1000):
        self.history: List[Dict[str, Any]] = []
        self.max_entries = max_entries
        self._current_index = 0

    def record_state(self, state: AgentState, timestamp: datetime = None):
        """Record a new state snapshot"""
        if timestamp is None:
            timestamp = datetime.now()
        
        state_dict = state.to_dict()
        state_dict['timestamp'] = timestamp.isoformat()
        
        self.history.insert(0, state_dict)
        
        if len(self.history) > self.max_entries:
            self.history.pop()

    def get_history(self) -> List[Dict[str, Any]]:
        """Get the complete state history"""
        return self.history[:self._current_index + 1].copy()

    def get_diff(self, start: int, end: int) -> Dict[str, Any]:
        """Get state differences between two points"""
        if start >= end or start < 0 or end > len(self.history):
            return {}
        
        start_state = self.history[start]
        end_state = self.history[end]
        
        diff = {}
        for key in set(start_state.keys()).union(set(end_state.keys())):
            start_val = start_state.get(key)
            end_val = end_state.get(key)
            if start_val != end_val:
                diff[key] = {
                    'from': start_val,
                    'to': end_val
                }
        return diff

    def find_state(self, predicate: callable) -> Dict[str, Any]:
        """Find states matching a predicate"""
        return [state for state in self.history if predicate(state)]

    def clear(self):
        """Clear all state history"""
        self.history.clear()
        self._current_index = 0