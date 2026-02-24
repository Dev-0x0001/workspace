# End-to-End Tests

# This directory contains tests that validate complete system workflows

# Example e2e test
import unittest
import requests

class TestAPIEndpoints(unittest.TestCase):
    def test_health_check(self):
        # Test health check endpoint
        response = requests.get('http://localhost:8000/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'healthy')

    def test_data_endpoint(self):
        # Test data retrieval
        response = requests.get('http://localhost:8000/api/data')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('items' in response.json())

if __name__ == '__main__':
    unittest.main()