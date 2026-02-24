```python
# System State Tracking Module

class AutonomousSystem:
    """Core system tracking the agent's state and goals."""

    def __init__(self):
        self.current_action = None
        self.next_action = None
        self.permanent_goal = None
        self.current_goal = None
        self.action_history = []
        self.short_term_memory = {}
        self.time = None

    def update_state(self, action_taken: str = None, **kwargs):
        """Update the system's state after an action."""
        if action_taken:
            self.action_history.append(action_taken)
        
        # Update state properties from kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Always reset next_action after action is taken
        self.next_action = None
        
        return self

    def plan_next_actions(self, *actions: str) -> 'AutonomousSystem':
        """Plan future actions to execute."""
        self.next_action = actions[0] if actions else None
        return self

    def set_permanent_goal(self, goal: str) -> 'AutonomousSystem':
        """Define a long-term objective for the agent."""
        self.permanent_goal = goal
        return self

    def set_current_goal(self, goal: str) -> 'AutonomousSystem':
        """Define the current working objective."""
        self.current_goal = goal
        return self

    def think(self, *args, **kwargs) -> 'AutonomousSystem':
        """Main thinking method to be implemented by subclasses."""
        raise NotImplementedError

    def act(self, *args, **kwargs) -> 'AutonomousSystem':
        """Main acting method to be implemented by subclasses."""
        raise NotImplementedError

    def __str__(self):
        return f"AutonomousSystem(
            current_action={self.current_action},
            next_action={self.next_action},
            permanent_goal={self.permanent_goal},
            current_goal={self.current_goal},
            action_history={self.action_history[-3:]},
            short_term_memory={dict(self.short_term_memory)},
            time={self.time}
        )"

    __repr__ = __str__
