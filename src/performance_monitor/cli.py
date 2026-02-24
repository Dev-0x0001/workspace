import argparse
import json
import sys
from datetime import datetime

from performance_monitor.baseline_comparison import BaselineComparator

def load_metrics(file_path):
    """Load metrics from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found", file=sys.stderr)
        sys.exit(1)

def main():
    """Entry point for command-line interface"""
    parser = argparse.ArgumentParser(
        description='Compare current metrics to baseline'`
    )
    parser.add_argument('--metrics', '-m', required=True, help='Path to current metrics JSON file')
    parser.add_argument('--baseline', '-b', default='baseline.json', help='Path to baseline file')
    parser.add_argument('--output', '-o', default='comparison_report.md', help='Output report file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    # Load current metrics
    current_metrics = load_metrics(args.metrics)
    
    # Initialize comparator
    comparator = BaselineComparator(args.baseline)
    
    # Calculate differences
    print(f"Comparing metrics... {datetime.now()}")
    diff = comparator.calculate_diff(current_metrics)
    
    # Generate report
    print(f"Generating report... {datetime.now()}")
    comparator.generate_report(diff, args.output)
    
    # Summary output
    print(f"
Comparison Complete: {datetime.now()}")
    print(f"- Baseline: {args.baseline}")
    print(f"- Metrics: {args.metrics}")
    print(f"- Output: {args.output}")
    
    if diff['summary']['total_changes'] == 0 and not diff['added'] and not diff['removed']:
        print("\nNo changes detected. System is performing as expected.")
    else:
        print(f"\nChanges detected: {diff['summary']['total_changes']}")
        
    # Return exit code based on changes
    sys.exit(1 if diff['summary']['total_changes'] > 0 else 0)

if __name__ == '__main__':
    main()