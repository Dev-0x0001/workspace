from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class Action:
    """
    Represents an action taken by the autonomous system.
    """
    name: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "pending"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "metadata": self.metadata.copy()
        }

    def __str__(self) -> str:
        return f"Action(name='{self.name}', status='{self.status}', timestamp='{self.timestamp}')"

@dataclass
class Goal:
    """
    Represents a goal, which can be permanent or current.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    priority: int = 0
    status: str = "active"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def __str__(self) -> str:
        return f"Goal(id='{self.id}', title='{self.title}', status='{self.status}')"

@dataclass
class SystemState:
    """
    Central state container for the autonomous system.
    """
    current_action: Optional[Action] = None
    next_action: Optional[Action] = None
    permanent_goal: Optional[Goal] = None
    current_goal: Optional[Goal] = None
    action_history: List[Action] = field(default_factory=list)
    short_term_memory: Dict[str, Any] = field(default_factory=dict)
    long_term_memory: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def update(self, **kwargs: Dict[str, Any]) -> "SystemState":
        """
        Update one or more state properties.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.timestamp = datetime.now()
        return self

    def take_action(self, action: Action) -> "SystemState":
        """
        Record an action being taken and update state.
        """
        self.action_history.append(action)
        self.current_action = action
        self.next_action = None
        self.timestamp = datetime.now()
        return self

    def complete_action(self) -> "SystemState":
        """
        Mark the current action as complete.
        """
        if self.current_action:
            self.current_action.status = "completed"
            self.current_action = None
        self.timestamp = datetime.now()
        return self

    def plan_next_actions(self, actions: List[Action]) -> "SystemState":
        """
        Plan future actions to execute.
        """
        self.next_action = actions[0] if actions else None
        self.timestamp = datetime.now()
        return self

    def set_goal(self, goal: Goal, is_permanent: bool = False) -> "SystemState":
        """
        Set either the current or permanent goal.
        """
        if is_permanent:
            self.permanent_goal = goal
        else:
            self.current_goal = goal
        self.timestamp = datetime.now()
        return self

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert state to dictionary for serialization.
        """
        return {
            "current_action": self.current_action.to_dict()
            if self.current_action else None,
            "next_action": self.next_action.to_dict()
            if self.next_action else None,
            "permanent_goal": self.permanent_goal.to_dict()
            if self.permanent_goal else None,
            "current_goal": self.current_goal.to_dict()
            if self.current_goal else None,
            "action_history": [action.to_dict() for action in self.action_history],
            "short_term_memory": self.short_term_memory.copy(),
            "long_term_memory": self.long_term_memory.copy(),
            "timestamp": self.timestamp.isoformat()
        }

    def __str__(self) -> str:
        return f"SystemState(
            current_action={self.current_action},
            next_action={self.next_action},
            permanent_goal={self.permanent_goal},
            current_goal={self.current_goal},
            action_history={len(self.action_history)} actions,
            memory={len(self.short_term_memory)} items)
        "

    __repr__ = __str__