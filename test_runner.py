import os
import sys
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import json
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

dataclass
class TestResult:
    """Results from a single inheritance test."""
    test_id: str
    description: str
    passed: bool
    details: Dict[str, Any]
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            'test_id': self.test_id,
            'description': self.description,
            'passed': self.passed,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }

dataclass
class TestSuite:
    """Collection of inheritance tests."""
    name: str
    tests: List[TestResult]
    total_tests: int
    passed_tests: int
    failed_tests: int
    timestamp: datetime

    @property
    def summary(self) -> str:
        return (
            f"Test Suite: {self.name}\n"
            f"Total Tests: {self.total_tests}\n"
            f"Passed: {self.passed_tests}\n"
            f"Failed: {self.failed_tests}\n"
        )

    def add_test(self, result: TestResult) -> 'TestSuite':
        """Add a test result to the suite."""
        self.tests.append(result)
        self.total_tests += 1
        if result.passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
        return self

    def save_results(self, filename: str) -> None:
        """Save test results to a file."""
        try:
            with open(filename, 'w') as f:
                json.dump(self.__dict__, f, default=str, indent=4)
            logger.info(f"Saved test results to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {str(e)}")

    @classmethod
    def load_results(cls, filename: str) -> 'TestSuite':
        """Load test results from a file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            suite = cls(
                name=data['name'],
                tests=[],
                total_tests=data['total_tests'],
                passed_tests=data['passed_tests'],
                failed_tests=data['failed_tests'],
                timestamp=datetime.fromisoformat(data['timestamp'])
            )
            suite.tests = data['tests']
            return suite
        except Exception as e:
            logger.error(f"Failed to load results: {str(e)}")
            return cls(
                name=data['name'],
                tests=[],
                total_tests=0,
                passed_tests=0,
                failed_tests=0,
                timestamp=datetime.now()
            )

def create_test_id(language: str, test_name: str) -> str:
    """Generate a unique test ID."""
    return f"{language}:{test_name}:{datetime.now().isoformat()}"

def run_test(language: str, test_name: str, code: str) -> TestResult:
    """Run a single inheritance test."""
    test_id = create_test_id(language, test_name)
    description = f"Test {test_name} in {language}"""

    try:
        # Create temporary file for test code
        temp_file = Path(f"temp_{test_id}.py")
        temp_file.write_text(code)

        # Execute the test
        result = subprocess.run(
            [sys.executable, str(temp_file)],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Analyze the result
        passed = result.returncode == 0
        details = {
            'return_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'test_code': code
        }

        logger.info(
            f"Test {test_id} - {\n'            f"Status: {'Passed' if passed else 'Failed'}\n"
            f"Output: {details['stdout'][:200]}..."
        )

        return TestResult(
            test_id=test_id,
            description=description,
            passed=passed,
            details=details,
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Test {test_id} failed with error: {str(e)}")
        return TestResult(
            test_id=test_id,
            description=description,
            passed=False,
            details={'error': str(e)},
            timestamp=datetime.now()
        )
    finally:
        # Clean up temporary file
        if temp_file.exists():
            temp_file.unlink()


def run_test_suite(suites: Dict[str, List[Dict[str, str]]]) -> Dict[str, TestSuite]:
    """Run multiple test suites."""
    results: Dict[str, TestSuite] = {}

    for suite_name, tests in suites.items():
        suite_results = TestSuite(
            name=suite_name,
            tests=[],
            total_tests=len(tests),
            passed_tests=0,
            failed_tests=0,
            timestamp=datetime.now()
        )

        for test in tests:
            language = test['language']
            test_name = test['test_name']
            code = test['code']

            result = run_test(language, test_name, code)
            suite_results = suite_results.add_test(result)

        results[suite_name] = suite_results

    return results
