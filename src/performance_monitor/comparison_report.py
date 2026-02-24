import json
import hashlib
from datetime import datetime
import difflib

class BaselineComparator:
    """Compares current state to baseline and generates detailed reports"""
     
    def __init__(self, baseline_file='baseline.json'):
        self.baseline_file = baseline_file
        self.current_state = {}
        self.baseline = self._load_baseline()
        
    def _load_baseline(self):
        """Load or create baseline file if it doesn't exist"""
        if os.path.exists(self.baseline_file):
            with open(self.baseline_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_baseline(self):
        """Save current state as new baseline"""
        with open(self.baseline_file, 'w') as f:
            json.dump(self.current_state, f, indent=4)

    def calculate_diff(self, current_data):
        """Calculate differences between current data and baseline"""
        self.current_state = current_data
        diff = {
            'changed': {},
            'added': [],
            'removed': [],
            'summary': {}
        }
        
        # Calculate changes for each metric type
        for metric_type in ['performance', 'security', 'efficiency']:
            if metric_type in self.current_state and metric_type in self.baseline:
                self._compare_metrics(diff, metric_type)
            elif metric_type in self.current_state and metric_type not in self.baseline:
                diff['added'].extend([f"{metric_type}: {k}" for k in self.current_state[metric_type]])
            elif metric_type not in self.current_state and metric_type in self.baseline:
                diff['removed'].extend([f"{metric_type}: {k}" for k in self.baseline[metric_type]])
        
        # Generate summary
        self._generate_summary(diff)
        
        return diff

    def _compare_metrics(self, diff, metric_type):
        """Compare individual metrics within a type"""
        baseline_metrics = self.baseline[metric_type]
        current_metrics = self.current_state[metric_type]
        
        changed_metrics = {}
        for metric, value in current_metrics.items():
            if metric in baseline_metrics:
                if value != baseline_metrics[metric]:
                    changed_metrics[metric] = {
                        'old': baseline_metrics[metric],
                        'new': value,
                        'difference': value - baseline_metrics[metric]
                    }
        
        if changed_metrics:
            diff['changed'][metric_type] = changed_metrics

    def _generate_summary(self, diff):
        """Create summary statistics for the diff"""
        summary = {
            'total_changes': 0,
            'performance_changes': 0,
            'security_changes': 0,
            'efficiency_changes': 0,
            'new_items': len(diff['added']),
            'removed_items': len(diff['removed'])
        }
        
        for metric_type in ['performance', 'security', 'efficiency']:
            if metric_type in diff['changed']:
                summary[f'{metric_type}_changes'] = len(diff['changed'][metric_type])
                summary['total_changes'] += len(diff['changed'][metric_type])
        
        diff['summary'] = summary

    def generate_report(self, diff, output_file='comparison_report.md'):
        """Generate human-readable report of changes"""
        with open(output_file, 'w') as f:
            f.write("# Performance Comparison Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if diff['summary']['total_changes'] == 0 and not diff['added'] and not diff['removed']:
                f.write("## No significant changes detected\n")
                return
            
            # Performance section
            if 'performance' in diff['changed']:
                f.write("## Performance Metrics\n")
                for metric, changes in diff['changed']['performance'].items():
                    sign = '+' if changes['difference'] > 0 else '-'
                    f.write(f"- **{metric}**: {sign}{abs(changes['difference']):.2f} (was {changes['old']:.2f})\n")
                f.write("\n")
            
            # Security section
            if 'security' in diff['changed']:
                f.write("## Security Vulnerabilities\n")
                for metric, changes in diff['changed']['security'].items():
                    f.write(f"- {metric}: \n")
                    f.write(f"  - Old: {changes['old']}\n")
                    f.write(f"  - New: {changes['new']}\n")
                    f.write(f"  - Change: {changes['difference']}\n")
                f.write("\n")
            
            # Efficiency section
            if 'efficiency' in diff['changed']:
                f.write("## Code Efficiency\n")
                for metric, changes in diff['changed']['efficiency'].items():
                    f.write(f"- **{metric}**: Improved by {changes['difference']}\n")
                f.write("\n")
            
            # Summary
            f.write("## Summary\n")
            f.write(f"- Total changes: {diff['summary']['total_changes']}\n")
            f.write(f"- New items: {diff['summary']['new_items']}\n")
            f.write(f"- Removed items: {diff['summary']['removed_items']}\n")

    def hash_content(self, content):
        """Generate hash for content - used for detecting changes"""
        return hashlib.sha256(content.encode()).hexdigest()

    def get_diff_text(self, current, baseline):
        """Get text diff between two versions"""
        return ''.join(difflib.Differ().compare(
            baseline.split('\n'),
            current.split('\n')
        )), {