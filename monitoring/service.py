# Monitoring Service
# This service collects and forwards metrics

import requests
import time

class MonitoringService:
    def __init__(self):
        self.prometheus_url = "http://localhost:9090"
        self.grafana_url = "http://localhost:3000"
        self.alert_manager_url = "http://localhost:9093"

    def check_alerts(self):
        """
        Check Prometheus for active alerts
        """
        try:
            response = requests.get(f"{self.prometheus_url}/api/v1/alerts")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error checking alerts: {e}")
            return None