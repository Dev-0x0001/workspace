import os
import json
from datetime import datetime

class ImprovementFramework:
    """Core class for managing the sustainable improvement process"""
    



    def __init__(self, project_name):
        self.project_name = project_name
        self.framework_file = os.path.join(os.getcwd(), 'docs', 'sustainable-improvement-framework.md')
        self.last_review = None
        self.review_history = []
        self.load_review_history()

    def load_review_history(self):
        """Load review history from disk or initialize if empty"""
        if os.path.exists('review_history.json'):
            with open('review_history.json', 'r') as f:
                self.review_history = json.load(f)
            if self.review_history:
                self.last_review = datetime.fromisoformat(self.review_history[-1]['review_date'])
        
    def save_review_history(self):
        """Save review history to disk"""
        with open('review_history.json', 'w') as f:
            json.dump(self.review_history, f, indent=4)

    def start_analysis_phase(self):
        """Initialize the analysis phase"""
        return {
            'status': 'analysis_started',
            'timestamp': datetime.now().isoformat(),
            'message': 'Analysis phase initiated for {}'.format(self.project_name)
        }

    def complete_analysis(self, findings):
        """Complete the analysis phase and return results"""
        result = {
            'status': 'analysis_complete',
            'timestamp': datetime.now().isoformat(),
            'findings': findings,
            'next_step': 'design_phase'
        }
        self._log_review_action('analysis', findings, 'completed')
        return result

    def _log_review_action(self, phase, details, status):
        """Internal method to log review actions"""
        action = {
            'date': datetime.now().isoformat(),
            'phase': phase,
            'details': details,
            'status': status
        }
        self.review_history.append(action)
        self.save_review_history()

    def get_review_status(self):
        """Get current review status"""
        if not self.review_history:
            return {
                'status': 'never_reviewed',
                'message': 'No review history exists for this framework'
            }
        
        latest = self.review_history[-1]
        return {
            'status': 'last_reviewed',
            'date': latest['date'],
            'phase': latest['phase'],
            'details': latest['details']
        }

    def approve_framework(self):
        """Approve the framework and update status"""
        approval = {
            'date': datetime.now().isoformat(),
            'status': 'approved',
            'message': 'Framework approved by review committee',
            'approved_by': os.getenv('USER', 'unknown')
        }
        self._log_review_action('approval', approval, 'completed')
        return approval

    def reject_framework(self, reasons):
        """Reject the framework with specific reasons"""
        rejection = {
            'date': datetime.now().isoformat(),
            'status': 'rejected',
            'reasons': reasons,
            'message': 'Framework requires significant revisions',
            'reviewed_by': os.getenv('USER', 'unknown')
        }
        self._log_review_action('approval', rejection, 'rejected')
        return rejection