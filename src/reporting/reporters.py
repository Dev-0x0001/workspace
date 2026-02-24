from abc import ABC, abstractmethod
from typing import Dict, Any

class Reporter(ABC):
    """Abstract base class for reporters."""

    @abstractmethod
def report_metrics(self, metrics: Dict[str, Any]) -> None:
        """Report metrics to destination."""
        pass


class ConsoleReporter(Reporter):
    """Reports metrics to console."""

    def report_metrics(self, metrics: Dict[str, Any]) -> None:
        print("=\*\* Metrics Report \*\*")
        for category, items in metrics.items():
            print(f"
Category: {category}")
            for key, value in items.items():
                print(f"- {key}: {value}")
        print("=\*\* End of Report \*\*")


class FileReporter(Reporter):
    """Reports metrics to file."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def report_metrics(self, metrics: Dict[str, Any]) -> None:
        with open(self.file_path, 'w') as f:
            f.write(str(metrics))


class EmailReporter(Reporter):
    """Reports metrics via email (example implementation)."""

    def __init__(self, email_config: Dict[str, Any]):
        self.email_config = email_config

    def report_metrics(self, metrics: Dict[str, Any]) -> None:
        # In practice, this would send an email
        print(f"Email reporter would send metrics to {self.email_config.get('to')}...")
        print(f"Metrics: {metrics}")


class SlackReporter(Reporter):
    """Reports metrics to Slack (example implementation)."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def report_metrics(self, metrics: Dict[str, Any]) -> None:
        # In practice, this would post to Slack
        print(f"Slack reporter would post to {self.webhook_url}...")
        print(f"Metrics: {metrics}")