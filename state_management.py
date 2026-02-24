from system_state import SystemState, Action, Goal
import json
from datetime import datetime

# ================
# State Management
# ================
def create_initial_state() -> SystemState:
    """
    Create a baseline system state with common initial configurations.
    """
    return SystemState(
        current_action=None,
        next_action=None,
        permanent_goal=Goal(
            title="Become world's most capable AI assistant",
            description="Continuously improve performance, reliability, and user value"
        ),
        current_goal=Goal(
            title="Understand user's specific requirements",
            description="Analyze the current request and determine best course of action"
        ),
        action_history=[],
        short_term_memory={}
    )

def update_state_from_dict(state: SystemState, update_data: Dict[str, Any]) -> SystemState:
    """
    Update system state from dictionary data.
    """
    return state.update(**update_data)

def serialize_state(state: SystemState) -> str:
    """
    Serialize the system state to JSON string.
    """
    return json.dumps(state.to_dict(), indent=2)
def deserialize_state(data: str) -> SystemState:
    """
    Deserialize JSON data back to system state.
    """
    return SystemState(**json.loads(data))

def reset_state(state: SystemState) -> SystemState:
    """
    Reset the system state to initial configuration.
    """
    return create_initial_state()

# ================
# Action Management
# ================
def create_action(name: str, **kwargs) -> Action:
    """
    Create a new action with optional metadata.
    """
    return Action(name=name, **kwargs)
def complete_action(state: SystemState, action_name: str) -> SystemState:
    """
    Complete an action by name if it exists in history.
    """
    if state.current_action and state.current_action.name == action_name:
        return state.complete_action()
    return state
def get_current_action(state: SystemState) -> Optional[Action]:
    """
    Retrieve the current action if one exists.
    """
    return state.current_action
def list_all_actions(state: SystemState) -> List[Action]:
    """
    Get a list of all actions (current + history).
    """
    return [state.current_action] + state.action_history if state.current_action else state.action_history

# ================
# Goal Management
# ================
def get_active_goal(state: SystemState) -> Optional[Goal]:
    """
    Get the currently active goal (permanent or current).
    """
    return state.current_goal or state.permanent_goal
def update_goal(state: SystemState, goal_type: str, **kwargs) -> SystemState:
    """
    Update properties of a specific goal type.
    """
    goal_attr = f"{goal_type}_goal"
    if hasattr(state, goal_attr) and getattr(state, goal_attr):
        for key, value in kwargs.items():
            setattr(getattr(state, goal_attr), key, value)
        setattr(state, goal_attr, getattr(state, goal_attr))
    return state