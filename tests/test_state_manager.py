import unittest
from src.agent.state_manager import StateManager

class TestStateManager(unittest.TestCase):
    """Tests for state manager."""

    def setUp(self):
        """Set up test environment."""
        self.state_manager = StateManager()

    def test_initial_state(self):
        """Test initial state."""
        self.assertEqual(self.state_manager.current_state, 'initial')
        self.assertEqual(self.state_manager.next_state, 'planning')

    def test_update_state(self):
        """Test state update method."""
        self.state_manager.update_state('executing', 'task_complete')
        self.assertEqual(self.state_manager.current_state, 'executing')
        self.assertEqual(self.state_manager.next_state, 'task_complete')

    def test_add_memory(self):
        """Test adding memory."""
        self.state_manager.add_memory('test_memory')
        self.assertIn('test_memory', self.state_manager.short_term_memory)

    def test_clear_memory(self):
        """Test clearing memory."""
        self.state_manager.add_memory('test_memory_1')
        self.state_manager.add_memory('test_memory_2')
        self.state_manager.clear_memory()
        self.assertEqual(len(self.state_manager.short_term_memory), 0)

if __name__ == '__main__':
    unittest.main()