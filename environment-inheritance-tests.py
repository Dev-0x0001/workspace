import unittest
from contextlib import contextmanager
import os
import subprocess
import tempfile
from typing import Dict, List, Optional
import json
from datetime import datetime

class EnvironmentInheritanceTest(unittest.TestCase):
    """
    Test suite for environment variable inheritance and shell startup behavior
    """

    @classmethod
    def setUpClass(cls):
        """Create temporary directory for test files"""
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_files = {
            'profile': '# Test profile
export TEST_PROFILE=profile_value
export PATH_MODIFY=${PATH}:/tmp/test-path-profile',
            'bashrc': '# Test bashrc
export TEST_BASHRC=bashrc_value',
            'local-bashrc': '# Local bashrc
export TEST_LOCAL_BASHRC=local_value',
        }
        
        # Create test files in temporary directory
        cls.test_file_paths = {}
        for name, content in cls.test_files.items():
            file_path = os.path.join(cls.temp_dir.name, f'test-{name}')
            with open(file_path, 'w') as f:
                f.write(content)
            cls.test_file_paths[name] = file_path
            
        # Set environment variables for tests
        os.environ['BASE_TEST_VAR'] = 'original_value'
        os.environ['PATH_MODIFY'] = os.environ['PATH']

    @classmethod
def tearDownClass(cls):
        """Clean up temporary directory"""
        cls.temp_dir.cleanup()

    @contextmanager
def captured_output(self):
        """Capture stdout and stderr"""
        import sys
        from io import StringIO
        
        new_out = StringIO()
        new_err = StringIO()
        old_out = sys.stdout
        old_err = sys.stderr
        try:
            sys.stdout = new_out
            sys.stderr = new_err
            yield new_out, new_err
        finally:
            sys.stdout = old_out
            sys.stderr = old_err

    def setUp(self):
        self.original_env = os.environ.copy()
        
    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.original_env)

    def assert_env_contains(self, expected_vars: Dict[str, str], env=None):
        """Assert environment contains expected variables"""
        if env is None:
            env = os.environ
        
        for var, expected_value in expected_vars.items():
            self.assertIn(var, env, f"Missing environment variable: {var}")
            self.assertEqual(env[var], expected_value, 
                             f"Value mismatch for {var}: expected {expected_value}, got {env[var]}")

    def assert_env_does_not_contain(self, excluded_vars: List[str], env=None):
        """Assert environment does not contain excluded variables"""
        if env is None:
            env = os.environ
        
        for var in excluded_vars:
            self.assertNotIn(var, env, f"Unexpected environment variable: {var}")

    def test_environment_inheritance(self):
        """Test basic environment inheritance between processes"""
        
        # Set initial environment
        os.environ['TEST_VAR'] = 'parent_value'
        
        # Test child process inheritance
        result = subprocess.run(['bash', '-c', 'echo $TEST_VAR'], 
                               capture_output=True, text=True)
        
        self.assertEqual(result.stdout.strip(), 'parent_value',
                         'Environment variable not inherited by child shell')
        self.assertEqual(result.stderr, '',
                         'No error output expected')

    def test_environment_modification(self):
        """Test environment modification in child process"""
        
        # Set initial value
        os.environ['TEST_VAR'] = 'parent_value'
        
        # Test modification in child shell
        result = subprocess.run(['bash', '-c', 
                                'export TEST_VAR="child_value"; echo $TEST_VAR'],
                               capture_output=True, text=True)
        
        self.assertEqual(result.stdout.strip(), 'child_value',
                         'Child process failed to modify environment variable')
        self.assertEqual(result.stderr, '',
                         'No error output expected')
        
        # Verify parent environment remains unchanged
        self.assertEqual(os.environ['TEST_VAR'], 'parent_value',
                         'Parent environment should not be modified')

I'll continue writing the test cases for environment inheritance. The next tests will focus on restricted environments and startup file processing.

I'll add methods to test how environment variables behave in non-interactive shells and when explicit environment limits are applied. Then I'll create tests that verify startup file execution and their impact on environment variables.

The tests will use subprocess to simulate different shell scenarios and validate variable behavior across various contexts. I'll make sure to cover edge cases like variable overriding, file precedence, and security restrictions.

After completing the test suite, I'll organize the test files and prepare for execution, ensuring all scenarios are thoroughly validated.
</think>

 {