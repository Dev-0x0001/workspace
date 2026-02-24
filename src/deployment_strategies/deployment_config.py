# Deployment Configuration and Strategies

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json

@dataclass
class DeploymentConfig:
    """Configuration for deployment strategies."""
    
    # Basic configuration
    service_name: str
    environment: str = "production"
    replicas: int = 1
    
    # Rolling deployment settings
    rolling_update: bool = True
    maxUnavailable: int = 1
    maxSurge: int = 1
    
    # Canary deployment settings
    canary_percentage: Optional[int] = None
    canary_service_name: Optional[str] = None
    
    # Blue/Green deployment settings
    blue_green: bool = False
    target_service_name: Optional[str] = None
    
    # Health check configuration
    health_check_path: str = "/health"
    health_check_port: int = 80
    initial_delay_seconds: int = 30
    period_seconds: int = 10
    timeout_seconds: int = 5
    success_threshold: int = 1
    
    # Retry settings
    max_retry_count: int = 3
    retry_backoff_seconds: int = 1

    def to_kubernetes_yaml(self) -> Dict[str, Any]:
        """Convert configuration to Kubernetes deployment spec."""
        return {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': self.service_name,
                'labels': {'environment': self.environment}
            },
            'spec': {
                'replicas': self.replicas,
                'strategy': {
                    'type': 'RollingUpdate' if self.rolling_update else 'Recreate',
                    'rollingUpdate': {\n                        'maxUnavailable': self.maxUnavailable,
                        'maxSurge': self.maxSurge
                    } if self.rolling_update else {}
                },
                'template': {
                    'metadata': {'labels': {'app': self.service_name}},
                    'spec': {
                        'containers': [{
                            'name': self.service_name,
                            'image': f"{self.service_name}:{self.environment}",
                            'ports': [{'containerPort': self.health_check_port}],
                            'livenessProbe': {
                                'httpGet': {
                                    'path': self.health_check_path,
                                    'port': self.health_check_port
                                },
                                'initialDelaySeconds': self.initial_delay_seconds,
                                'periodSeconds': self.period_seconds,
                                'timeoutSeconds': self.timeout_seconds,
                                'successThreshold': self.success_threshold
                            },
                            'readinessProbe': {
                                'httpGet': {
                                    'path': self.health_check_path,
                                    'port': self.health_check_port
                                },
                                'initialDelaySeconds': self.initial_delay_seconds,
                                'periodSeconds': self.period_seconds,
                                'timeoutSeconds': self.timeout_seconds,
                                'successThreshold': self.success_threshold
                            }
                        }]
                    }
                }
            }
        }

    def generate_canary_config(self) -> Dict[str, Any]:
        """Generate canary deployment configuration."""
        if not self.canary_percentage:
            raise ValueError("Canary percentage must be set")
        
        config = self.to_kubernetes_yaml()
        
        # Modify for canary deployment
        config['spec']['template']['metadata']['labels']['canary'] = "true"
        config['spec']['template']['metadata']['annotations'] = {
            'canary.weight': str(self.canary_percentage)
        }
        
        if self.canary_service_name:
            config['metadata']['name'] = self.canary_service_name
        
        return config

    def generate_blue_green_config(self, target_service: str) -> Dict[str, Any]:
        """Generate blue/green deployment configuration."""
        if not self.target_service_name:
            raise ValueError("Target service name must be specified")
        
        config = self.to_kubernetes_yaml()
        
        # Blue/Green specific configuration
        config['metadata']['name'] = f"{self.service_name}-blue"
        config['spec']['template']['metadata']['labels']['environment'] = "blue"
        
        # Service for blue/green
        service_config = {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {
                'name': self.service_name
            },
            'spec': {
                'ports': [{'port': 80, 'targetPort': self.health_check_port}],
                'selector': {'app': self.service_name, 'environment': 'blue'}
            }
        }
        
        return {
            'deployment': config,
            'service': service_config
        }
