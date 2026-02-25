import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime

class State:
    """Represents the current state of the system"""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return self.__dict__.copy()

    def update(self, **kwargs):
        self.__dict__.update(kwargs)
        return self

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'State':
        return State(**data)


dataclass(kw_only=True)
class Goal:
    """Represents a goal with priority and completion status"""

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str
    description: Optional[str] = None
    priority: int = 1
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def mark_complete(self):
        self.completed = True
        self.updated_at = datetime.now()

    def to_dict(self):
        return self.__dict__.copy()


dataclass(kw_only=True)
class Action:
    """Represents an action to take"""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    required_parameters: List[str] = field(default_factory=list)
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return self.__dict__.copy()


dataclass(kw_only=True)
class PlanningResult:
    """Result of a planning session"""

    plan: List[Action] = field(default_factory=list)
    rationale: str = ""
    confidence: float = 0.0

    def to_dict(self):
        return self.__dict__.copy()


dataclass(kw_only=True)
class Session:
    """Represents a planning session"""

    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    input_state: State = field(default_factory=State)
    output_state: State = field(default_factory=State)
    plan: List[Action] = field(default_factory=list)
    result: Optional[PlanningResult] = None

    def execute_plan(self) -> Optional[PlanningResult]:
        """Execute the plan and return results"""
        if not self.plan:
            return None

        results = []
        for action in self.plan:
            try:
                # Execute action
                # This is a placeholder - actual execution would modify state
                results.append({