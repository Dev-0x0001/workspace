import unittest
from datetime import datetime
from dataclasses import dataclass, field
import json

@dataclass
class MockAction:
    name: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "pending"

@dataclass
class MockGoal:
    id: str = ""
    title: str = ""

class TestSystemState(unittest.TestCase):
    
    def setUp(self):
        self.state = SystemState()
        self.mock_action = MockAction("Test Action")
        self.mock_goal = MockGoal()

    def test_initial_state(self):
        self.assertIsNone(self.state.current_action)
        self.assertIsNone(self.state.next_action)
        self.assertIsNone(self.state.permanent_goal)
        self.assertIsNone(self.state.current_goal)
        self.assertEqual(len(self.state.action_history), 0)
        self.assertEqual(self.state.short_term_memory, {})

    def test_update_method(self):
        # Test updating multiple properties
        self.state.update(
            current_action=self.mock_action,
            short_term_memory={"test_key": "test_value"}
        )
        
        self.assertEqual(self.state.current_action, self.mock_action)
        self.assertEqual(self.state.short_term_memory["test_key"], "test_value")
        
        # Test timestamp updates
        initial_timestamp = self.state.timestamp
        self.state.update()
        self.assertGreater(self.state.timestamp, initial_timestamp)

    def test_take_action(self):
        self.state.take_action(self.mock_action)
        
        self.assertEqual(self.state.current_action, self.mock_action)
        self.assertIsNone(self.state.next_action)
        self.assertEqual(len(self.state.action_history), 1)
        self.assertEqual(self.state.action_history[0], self.mock_action)

    def test_complete_action(self):
        self.state.take_action(self.mock_action)
        
        self.state.complete_action()
        self.assertIsNone(self.state.current_action)
        self.assertEqual(self.mock_action.status, "completed")

    def test_plan_next_actions(self):
        actions = [
            MockAction("Action 1"),
            MockAction("Action 2")
        ]
        self.state.plan_next_actions(actions)
        
        self.assertEqual(self.state.next_action, actions[0])
        self.assertEqual(len(self.state.action_history), 0)

    def test_set_goal(self):
        self.state.set_goal(self.mock_goal, is_permanent=True)
        self.assertEqual(self.state.permanent_goal, self.mock_goal)
        
        self.state.set_goal(MockGoal("New Current Goal"), is_permanent=False)
        self.assertEqual(self.state.current_goal.title, "New Current Goal")

    def test_to_dict_serialization(self):
        self.state.take_action(self.mock_action)
        self.state.set_goal(self.mock_goal, is_permanent=True)
        
        state_dict = self.state.to_dict()
        
        self.assertIn("current_action", state_dict)
        self.assertIn("permanent_goal", state_dict)
        self.assertIn("action_history", state_dict)
        self.assertGreater(len(state_dict["action_history"]), 0)

    def test_string_representation(self):
        print(self.state)
        self.assertIn("SystemState(", str(self.state))
        self.assertIn("current_action=None", str(self.state))

if __name__ == '__main__':
    unittest.main()