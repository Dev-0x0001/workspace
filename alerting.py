from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class MetricAlert:
    """Configuration for a metric alert"""
    metric_name: str
    threshold: float
    comparison: str  # 'greater_than', 'less_than', etc.
    severity: str
    description: str = ""

@dataclass
class AlertConfiguration:
    """Container for all alert configurations"""
    alerts: List[MetricAlert] = field(default_factory=list)

    def add_alert(self, alert: MetricAlert):
        self.alerts.append(alert)

    def check_alerts(self, metrics: Dict[str, float]) -> List[Dict[str, any]]:
        """Check which alerts are triggered"""
        triggered = []
        
        for alert in self.alerts:
            metric_value = metrics.get(alert.metric_name, 0)
            
            if alert.comparison == "greater_than" and metric_value > alert.threshold:
                triggered.append({
                    "alert": alert.metric_name,
                    "value": metric_value,
                    "threshold": alert.threshold,
                    "severity": alert.severity,
                    "timestamp": datetime.now().isoformat()
                })
            elif alert.comparison == "less_than" and metric_value < alert.threshold:
                triggered.append({
                    "alert": alert.metric_name,
                    "value": metric_value,
                    "threshold": alert.threshold,
                    "severity": alert.severity,
                    "timestamp": datetime.now().isoformat()
                })
        
        return triggered