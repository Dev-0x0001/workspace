from contextlib import contextmanager
import time

from .metrics import metrics_service

@contextmanager
def track_request(request_id: str):
    """Context manager to track request metrics"""
    metrics = metrics_service.track_request(request_id)
    try:
        yield metrics
    finally:
        metrics.record_end()

@contextmanager
def measure_latency(name: str = "inference"):
    """Context manager to measure latency"""
    start = time.time()
    try:
        yield start
    finally:
        duration = time.time() - start
        # ... record latency metrics ...

@contextmanager
def track_memory(name: str = "request"):
    """Context manager to track memory usage"""
    # Get memory snapshot before operation
    snapshot = metrics_service.get_memory_snapshot()
    try:
        yield snapshot
    finally:
        # Calculate memory usage
        pass