import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any

# Test Results Aggregator
class ResultsAggregator:
    """Aggregate test results from multiple sources."""
    
    @staticmethod
    def combine_results(*suite_results: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Combine multiple test suite results into one comprehensive report."""
        combined = {})
        
        for suite in suite_results:
            for suite_name, suite_data in suite.items():
                if suite_name not in combined:
                    combined[suite_name] = {
                        'total_tests': 0,
                        'passed_tests': 0,
                        'failed_tests': 0,
                        'timestamp': datetime.now(),
                        'details': []
                    }
                
                combined[suite_name]['total_tests'] += suite_data['total_tests']
                combined[suite_name]['passed_tests'] += suite_data['passed_tests']
                combined[suite_name]['failed_tests'] += suite_data['failed_tests']
                combined[suite_name]['details'].extend(suite_data['details'])
        
        return combined

    @staticmethod
    def generate_html_report(results: Dict[str, Dict[str, Any]], filename: str = 'report.html') -> str:
        """Generate an HTML report from test results."""
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Inheritance Security Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                h1 { color: #333; }
                .suite { margin-bottom: 40px; }
                .test { background: #f9f9f9; margin-bottom: 10px; padding: 15px; border-radius: 5px; }
                .passed { color: green; }
                .failed { color: red; }
            </style>
        </head>
        <body>
            <h1>Inheritance Security Test Report</h1>
        """
        
        for suite_name, suite_data in results.items():
            html_content += f"<div class='suite'>\n                <h2>{suite_name}</h2>\n                <p>Total Tests: {suite_data['total_tests']}</p>\n                <p>Passed: {suite_data['passed_tests']}</p>\n                <p>Failed: {suite_data['failed_tests']}</p>\n                <div class='tests'>"
            
            for test in suite_data['details']:
                status_class = 'passed' if test['passed'] else 'failed'
                html_content += f"\n                    <div class='test {status_class}'>\n                        <h3>{test['test_id']}</h3>\n                        <p><strong>Description:</strong> {test['description']}</p>\n                        <p><strong>Status:</strong> {'Passed' if test['passed'] else 'Failed'}</p>\n                        <p><strong>Details:</strong></p>\n                        <pre>{json.dumps(test['details'], indent=2)}</pre>\n                    </div>"
            
            html_content += "</div></div>"
        
        html_content += "</body></html>"

        try:
            with open(filename, 'w') as f:
                f.write(html_content)
            return f"Report generated successfully: {filename}"\n        except Exception as e:\n            return f"Failed to generate report: {str(e)}"
