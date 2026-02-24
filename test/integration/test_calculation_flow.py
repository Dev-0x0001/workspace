# Integration Tests

# This directory contains tests that verify interactions between components

# Example integration test
import unittest
from services import calculation_service

class TestIntegration(unittest.TestCase):
    def test_full_workflow(self):
        # Test complete workflow
        result = calculation_service.process_data({