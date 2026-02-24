import json
from datetime import datetime

# Metric configuration
METRIC_CONFIG = {
    'system': ['cpu_usage', 'memory_usage', 'disk_usage'],
    'process': ['python_memory', 'gc_collections'],
    'task': ['operations_processed', 'errors', 'duration']
}

# Capture baseline metrics
def capture_baseline(iteration_id):
    timestamp = datetime.now().isoformat()
    metrics = {'timestamp': timestamp, 'iteration': iteration_id}
    # Simulate metric collection
    for category, probes in METRIC_CONFIG.items():
        metrics[category] = {probe: 0 for probe in probes}
    return metrics