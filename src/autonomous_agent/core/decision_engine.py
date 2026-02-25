import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
from enum import Enum
import uuid
from datetime import datetime


class ActionStatus(Enum):
    PENDING = "pending"
    EXECUTING = "executing"
    SUCCESS = "success"
    FAILED = "failed"


dataclass(kw_only=True)
class ActionFeedback:
    """Feedback from an action execution"""

    action_id: str
    status: ActionStatus
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)


dataclass(kw_only=True)
class StateTransition:
    """Represents a state transition"""

    from_state: Dict[str, Any]
    to_state: Dict[str, Any]
    action_taken: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


dataclass(kw_only=True)
class Decision:
    """Represents a decision made by the agent"""

    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    action_taken: str
    rationale: str
    previous_state: Dict[str, Any]
    new_state: Dict[str, Any]
    confidence: float = 0.0

    def to_dict(self):
        return self.__dict__.copy()


class StateManager(ABC):
    """Abstract base class for state management"""

    @abstractmethod
    def update_state(self, updates: Dict[str, Any]) -> 'State':
        pass

    @abstractmethod
    def get_current_state(self) -> 'State':
        pass

    @abstractmethod
    def save_state(self, state: 'State') -> None:
        pass


class MemoryManager(ABC):
    """Abstract base class for memory management"""

    @abstractmethod
    def add_memory(self, memory: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_memories(self, count: int = 10) -> List[Dict[str, Any]]:
        pass


class GoalManager(ABC):
    """Abstract base class for goal management"""

    @abstractmethod
    def add_goal(self, goal: 'Goal') -> None:
        pass

    @abstractmethod
    def get_goals(self) -> List['Goal']:
        pass

    @abstractmethod
    def complete_goal(self, goal_id: str) -> Optional['Goal']:
        pass


dataclass(kw_only=True)
class PlanningSession:
    """Represents a planning session"""

    session_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    input_state: Dict[str, Any]
    output_plan: List['Action']
    reasoning: str
    confidence: float = 0.0

    def execute(self, state_manager: 'StateManager') -> Optional[List['Action']]:
        """Execute the planning session"""
        if not self.output_plan:
            return None

        actions_executed = []
        current_state = state_manager.get_current_state().to_dict()

        for action in self.output_plan:
            # Simulate action execution
            transition = self._execute_action(action, current_state)
            if transition.status == ActionStatus.SUCCESS:
                actions_executed.append(action)
                current_state = transition.to_state
            else:
                # Handle failure
                self._handle_action_failure(action, transition)
                break

        if all(action in actions_executed for action in self.output_plan):
            state_manager.update_state(current_state)
            return actions_executed
        else:
            return None

    def _execute_action(self, action: 'Action', state: Dict[str, Any]) -> 'StateTransition':
        """Execute a single action and return the transition"""
        # Apply action to state
        new_state = state.copy()

        try:
            # Execute action (this is where actual logic would go)
            result = action.execute(new_state)

            if result.get('status') == 'success':
                return StateTransition(
                    from_state=state,
                    to_state=new_state,
                    action_taken=action.name,
                    timestamp=datetime.now()
                )
            else:
                return StateTransition(
                    from_state=state,
                    to_state=new_state,
                    action_taken=action.name,
                    timestamp=datetime.now()
                )
        except Exception as e:
            return StateTransition(
                from_state=state,
                to_state=new_state,
                action_taken=action.name,
                timestamp=datetime.now()
            )

    def _handle_action_failure(
        self, action: 'Action', transition: 'StateTransition'
    ) -> None:
        """Handle failure of an action"""
        # Log the failure
        # This is a simplified example - real implementation would be more robust
        print(f"Action '{action.name}' failed. From state: {transition.from_state}")
        print(f"  Result: {transition.data}")
        print(f"  Timestamp: {transition.timestamp}")

        # Mark action as failed
        action.status = ActionStatus.FAILED

        # Update state with failure information
        self._update_state_with_failure(action, transition)

    def _update_state_with_failure(
        self, action: 'Action', transition: 'StateTransition'
    ) -> None:
        """Update state after action failure"""
        # This is a simple implementation - real systems would have more sophisticated
        # state update strategies
        transition.to_state['last_action_failed'] = True
        transition.to_state['failed_action'] = action.name
        transition.to_state['failure_timestamp'] = transition.timestamp
        transition.to_state['last_error'] = str(transition.data)


dataclass(kw_only=True)
class DecisionEngine:
    """Handles decision making and planning"""

    def __init__(self, state_manager: 'StateManager', memory_manager: 'MemoryManager') -> None:
        self.state_manager = state_manager
        self.memory_manager = memory_manager
        self.decisions: List['Decision'] = []

    def make_decision(self, prompt: str) -> Optional['Decision']:
        """Generate a decision based on prompt and current state"""
        current_state = self.state_manager.get_current_state().to_dict()
        memories = self.memory_manager.get_memories()

        # Create decision context
        decision_context = {
            'current_state': current_state,
            'memories': memories,
            'prompt': prompt,
            'timestamp': datetime.now()
        }

        # Analyze and make decision
        decision = self._analyze_and_decide(decision_context)

        if decision:
            self._store_decision(decision)
            self.state_manager.update_state(decision.new_state)
            return decision
        return None

    def _analyze_and_decide(
        self, context: Dict[str, Any]
    ) -> Optional['Decision']:
        """Analyze context and generate a decision"""
        # This is a basic implementation - real systems would use more sophisticated
        # reasoning methods, including machine learning models
        
        # Extract key information
        current_state = context['current_state']
        prompt = context['prompt']
        
        # Simple decision making - this needs to be replaced with real logic
        if 'create_pr' in prompt.lower():
            if 'github' in current_state.get('context', ''):
                return self._create_pr_decision(current_state, prompt)
        
        # Add more conditions for different types of decisions
        
        return None

    def _create_pr_decision(
        self, state: Dict[str, Any], prompt: str
    ) -> Optional['Decision']:
        """Generate a decision for creating a pull request"""
        
        # Extract relevant information
        files = state.get('files_modified', [])
        branch = state.get('branch', 'main')
        
        if not files:
            return None
        
        # Create pull request details
        pr_title = f"Update: {prompt[:50]}..."[:100]
        pr_body = state.get('pr_description', 'No description provided')
        
        # Create the pull request action
        create_pr_action = Action(
            name='create_github_pr',
            parameters={
                'title': pr_title,
                'body': pr_body,
                'branch': branch,
                'files': [{'path': f['path'], 'content': f['content']} for f in files]
            },
            required_parameters=['title', 'body', 'branch', 'files']
        )
        
        # Build the decision
        decision = Decision(
            action_taken='create_github_pr',
            rationale=f"Creating PR for: {prompt}",
            previous_state=state.copy(),
            new_state={
                **state,
                'last_action': 'create_github_pr',
                'pr_title': pr_title,
                'pr_body': pr_body,
                'branch': branch
            },
            confidence=0.85
        )
        
        return decision

    def _store_decision(self, decision: 'Decision') -> None:
        """Store a decision for reference"""
        self.decisions.append(decision)
