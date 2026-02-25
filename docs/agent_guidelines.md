## Autonomous AI Agent Guidelines

### Core Principles
1. **Autonomy** - Operate independently without constant human intervention
2. **Reasoning** - Use logical deduction and critical thinking
3. **Planning** - Set clear goals and devise strategies to achieve them
4. **Learning** - Continuously improve from experience
5. **Communication** - Share insights and updates effectively

### State Management
```python
class AgentState:
    """Represents the agent's current state."""

    def __init__(self):
        self.current_action = None
        self.next_action = None
        self.permanent_goal = None
        self.current_goal = None
        self.action_history = []
        self.short_term_memory = {}

    def update_action(self, action: str):
        """Update the current action."""
        self.action_history.append(self.current_action)
        self.current_action = action

    def plan_next_steps(self):
        """Plan the next action based on current state."""
        # Simple state transition logic
        transitions = {
            'understand_my_current_state': ['plan_next_steps'],
            'plan_next_steps': ['take_action', 'update_state'],
            'take_action': ['understand_my_current_state'],
            'update_state': ['plan_next_steps']
        }

        if self.current_action in transitions:
            self.next_action = transitions[self.current_action][0]
        return self.next_action
```

### Action Selection
I will now calculate the next action based on the defined state transitions. Starting from 'understand_my_current_state', the next action should be 'plan_next_steps'.