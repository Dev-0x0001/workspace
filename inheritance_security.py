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


# Test Definitions
TEST_SUITE = {
    "object_oriented": [
        {
            "language": "python",
            "test_name": "privilegeescalation",
            "code": """
import unittest

class BaseClass:
    def __init__(self):
        self.secure_data = 'sensitive_info'
        self.admin_access = False

    def grant_admin(self):
        self.admin_access = True
        return self.admin_access

class VulnerableChild(BaseClass):
    def __init__(self):
        super().__init__()

    def escalate_privileges(self):
        return self.grant_admin()

class TestInheritanceSecurity(unittest.TestCase):
    def test_privilege_escalation(self):
        base = BaseClass()
        self.assertFalse(base.admin_access, "Base class should not have admin access by default")

        child = VulnerableChild()
        self.assertFalse(child.admin_access, "Child class should not have admin access by default")

        # Test if child can escalate
        escalated = child.escalate_privileges()
        self.assertTrue(escalated, "Child should be able to escalate privileges")
        self.assertTrue(child.admin_access, "Privilege escalation failed")

    def test_data_protection(self):
        base = BaseClass()
        self.assertEqual(base.secure_data, 'sensitive_info')

        child = VulnerableChild()
        self.assertEqual(child.secure_data, 'sensitive_info')

if __name__ == '__main__':
    unittest.main()
""")
        },
        {
            "language": "python",
            "test_name": "methodoverriding",
            "code": """
import unittest

class BaseClass:
    def sensitive_operation(self):
        return "This is sensitive data"

class OverridingChild(BaseClass):
    def sensitive_operation(self):
        return "This is sensitive data"  # Same return value

class SecurityTest(unittest.TestCase):
    def test_method_overriding(self):
        base = BaseClass()
        child = OverridingChild()
        self.assertEqual(
            base.sensitive_operation(),
            child.sensitive_operation(),
            "Overridden method should return same value"
        )

class DangerousChild(BaseClass):
    def sensitive_operation(self):
        return "Hacked!"  # Different return value

    def attack(self):
        return self.sensitive_operation()

class AttackTest(unittest.TestCase):
    def test_method_overriding_attack(self):
        dangerous = DangerousChild()
        self.assertEqual(
            dangerous.sensitive_operation(),
            "Hacked!",
            "Method overriding changed behavior"
        )

def main():
    unittest.main()

if __name__ == "__main__":
    main()
""")
        }
    ],
    "prototype_based": [
        {
            "language": "javascript",
            "test_name": "propertyaccess",
            "code": """
// Prototype-based inheritance security test
// Tests if prototype properties are accessible securely

function BaseObject() {
    this.secureData = 'sensitive_info';
    this._internal = 'protected_data';
}

BaseObject.prototype.getSecureData = function() {
    return this.secureData;
};

BaseObject.prototype._getInternal = function() {
    return this._internal;
};

function ChildObject() {
    BaseObject.apply(this, arguments);
}

ChildObject.prototype = Object.create(BaseObject.prototype);
ChildObject.prototype.constructor = ChildObject;

ChildObject.prototype.getSecureData = function() {
    // Should return same value
    return this.secureData;
};

ChildObject.prototype._getInternal = function() {
    // Should access parent's protected method
    return BaseObject.prototype._getInternal.call(this);
};

// Test suite
(function(runner) {
    function TestCase(name, testFunction) {
        this.name = name;
        this.testFunction = testFunction;
    }

    TestCase.prototype.run = function() {
        try {
            this.testFunction();
            console.log(`✓ ${this.name} passed`);
            return true;
        } catch (e) {
            console.log(`✗ ${this.name} failed: ${e.message}`);
            return false;
        }
    };

    function TestSuite(name, tests) {
        this.name = name;
        this.tests = tests;
    }

    TestSuite.prototype.runAll = function() {
        console.log(`Running suite: ${this.name}`);
        let passed = 0;
        let failed = 0;
        for (const test of this.tests) {
            const result = test.run();
            if (result) passed++;
            else failed++;
        }
        console.log(
            `Suite ${this.name} complete: ${passed} passed, ${failed} failed`
        );
        return { passed, failed };
    };

    // Individual tests
    const tests = [
        new TestCase("Prototype property access", function() {
            const child = new ChildObject();
            console.assert(
                child.getSecureData() === 'sensitive_info',
                'Secure data access failed'
            );
        }),
        new TestCase("Protected method access", function() {
            const child = new ChildObject();
            console.assert(
                child._getInternal() === 'protected_data',
                'Protected method access failed'
            );
        }),
        new TestCase("Prototype modification attack", function() {
            const child = new ChildObject();
            // Try to modify prototype directly
            ChildObject.prototype.getSecureData = function() {
                return 'hacked_data';
            };
            console.assert(
                child.getSecureData() === 'hacked_data',
                'Prototype modification defense failed'
            );
        })
    ];

    // Run tests
    const suite = new TestSuite("Prototype Inheritance Security", tests);
    suite.runAll();
})();
""")
        }
    ],
    "mixin_based": [
        {
            "language": "python",
            "test_name": "accesscontrol",
            "code": """
import unittest

class AccessControlMixin:
    def __init__(self):
        self._secure_data = 'sensitive_info'
        self._access_granted = False

    def grant_access(self, password: str) -> bool:
        # Simple password check for demonstration
        return password == 'secure_password'

    def _get_secure_data(self) -> str:
        if not self._access_granted:
            raise PermissionError("Access denied")
        return self._secure_data

class DataProcessor(AccessControlMixin):
    def __init__(self):
        super().__init__()
        self.processed_data = []

    def process(self, password: str, data: str) -> List[str]:
        if self.grant_access(password):
            self._access_granted = True
            # Process data (simple example: split and return)
            return data.split()
        raise PermissionError("Access denied")

    def get_secure_data(self) -> str:
        return self._get_secure_data()

class TestMixinSecurity(unittest.TestCase):
    def test_access_control(self):
        processor = DataProcessor()
        
        # Test denied access
        with self.assertRaises(PermissionError):
            processor.get_secure_data()
        
        # Test successful access
        self.assertTrue(processor.grant_access('secure_password'))
        self.assertEqual(processor.get_secure_data(), 'sensitive_info')
        
        # Test failed access attempt
        with self.assertRaises(PermissionError):
            processor.get_secure_data()  # Should still require explicit grant

    def test_data_processing(self):
        processor = DataProcessor()
        
        # Test processing with correct password
        result = processor.process('secure_password', 'hello security')
        self.assertEqual(result, ['hello', 'security'])
        
        # Test processing with incorrect password
        with self.assertRaises(PermissionError):
            processor.process('wrong_password', 'test data')

if __name__ == '__main__':
    unittest.main()
""")
        }
    ]
}

# Runner
if __name__ == "__main__":
    from inheritance_security import run_test_suite
    results = run_test_suite(TEST_SUITE)
    for suite_name, suite in results.items():
        print(suite.summary())
        for test in suite.tests:
            print(f"  {test.test_id}: {\n'            f"    Passed: {test.passed}\n"
            f"    Details: {test.details['return_code']}")
