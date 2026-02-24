from datetime import datetime
from typing import Dict, List, Any
import json

class ReportGenerator:
    """Handles report generation in multiple formats."""

    @staticmethod
    def generate_text_report(metrics: Dict[str, Any]) -> str:
        """Generate a plain text report from metrics."""
        report = []
        report.append("=\*\* System Performance Report \*\*")
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 40)

        for category, items in metrics.items():
            report.append(f"
Section: {category.capitalize()}")
            report.append("-" * 30)
            for key, value in items.items():
                report.append(f"- {key}: {value}")

        return "\n".join(report)

    @staticmethod
    def generate_json_report(metrics: Dict[str, Any]) -> str:
        """Generate a JSON report from metrics."""
        return json.dumps(metrics, indent=4)

    @staticmethod
    def generate_html_report(metrics: Dict[str, Any]) -> str:
        """Generate an HTML report from metrics."""
        html = "<!DOCTYPE html>
<html>
<head>
    <title>System Performance Report</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h1, h2 { color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
        th { background-color: #f2f2f2; }
        .metric { margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>\n"

        html += f"<h2>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h2>\n"

        for category, items in metrics.items():
            html += f"<h2>{category.capitalize()}</h2>\n"
            html += "<div class='metric'>\n"
            html += "<table>\n"
            html += "<tr><th>Metric</th><th>Value</th></tr>\n"
            for key, value in items.items():
                html += f"<tr><td>{key}</td><td>{value}</td></tr>\n"
            html += "</table></div>\n"

        html += "</body>
</html>"
        return html