import unittest
from datetime import datetime

class TestSystemState(unittest.TestCase):
    
    def setUp(self):
        self.system = AutonomousSystem()
        self.system.time = datetime(2026, 2, 24, 19, 30, 8)

    def test_initial_state(self):
        self.assertIsNone(self.system.current_action)
        self.assertIsNone(self.system.next_action)
        self.assertIsNone(self.system.permanent_goal)
        self.assertIsNone(self.system.current_goal)
        self.assertEqual(self.system.action_history, [])
        self.assertEqual(self.system.short_term_memory, {})

    def test_update_state(self):
        # Test basic state update
        self.system.update_state(
            action_taken="Analyze user request",
            current_action="Processing goals",
            current_goal="Understand user's request"
        )
        
        self.assertEqual(self.system.current_action, "Processing goals")
        self.assertIsNone(self.system.next_action)
        self.assertEqual(self.system.action_history, ["Analyze user request"])
        
        # Test memory update
        self.system.update_state(memory={"analysis_complete": True})
        self.assertTrue(self.system.short_term_memory.get("analysis_complete"))

    def test_plan_next_actions(self):
        self.system.plan_next_actions("Identify key requirements", "Propose solutions")
        self.assertEqual(self.system.next_action, "Identify key requirements")
        
        # After action is taken, next_action should clear
        self.system.update_state(action_taken="Identify key requirements")
        self.assertIsNone(self.system.next_action)

    def test_set_goals(self):
        self.system.set_permanent_goal("Become world's best AI assistant")
        self.system.set_current_goal("Understand user's specific needs")
        
        self.assertEqual(self.system.permanent_goal, "Become world's best AI assistant")
        self.assertEqual(self.system.current_goal, "Understand user's specific needs")

    def test_string_representation(self):
        expected = "AutonomousSystem(\n            current_action=None,\n            next_action=None,\n            permanent_goal=None,\n            current_goal=None,\n            action_history=[],\n            short_term_memory={},\n            time=2026-02-24 19:30:08\n        )"
        self.assertEqual(str(self.system), expected)

if __name__ == '__main__':
    unittest.main()