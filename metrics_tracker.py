from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import time
import tracemalloc
import psutil
import os
import threading
from collections import deque

@dataclass
class LatencyMetrics:
    """Metrics for measuring inference latency"""
    
    # Request processing times
    prompt_token_latency: float = 0.0
    generation_token_latency: float = 0.0
    total_inference_latency: float = 0.0
    
    # Token processing statistics
    tokens_per_second: float = 0.0
    
    # Percentiles for distribution analysis
    p50_latency: float = 0.0
    p95_latency: float = 0.0
    p99_latency: float = 0.0
    
    # Rate limits
    request_rate: float = 0.0
    tokens_per_request: float = 0.0

@dataclass
class MemoryMetrics:
    """Metrics for tracking memory usage"""
    
    # Absolute measurements
    peak_memory: int = 0
    current_memory: int = 0
    
    # Model specific
    model_peak: int = 0
    model_current: int = 0
    
    # Cache usage
    cache_peak: int = 0
    cache_current: int = 0
    
    # GC statistics
    allocations: int = 0
    deallocations: int = 0
    
    # Memory pressure
    page_faults: int = 0
    swapped_out: int = 0

@dataclass
class RequestMetrics:
    """Metrics tracked per request"""
    
    request_id: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    # Latency breakdown
    load_input_latency: float = 0.0
    parse_input_latency: float = 0.0
    inference_latency: float = 0.0
    
    # Memory snapshot
    memory_before: int = 0
    memory_after: int = 0
    
    # Token statistics
    input_tokens: int = 0
    output_tokens: int = 0
    
    # Status information
    status: str = "pending"
    error: Optional[str] = None
    
    def record_end(self):
        self.end_time = datetime.now()
        self.status = "completed"

class MetricsService:
    """Central metrics service for tracking performance"""
    
    def __init__(self, service_name: str = "inference-service"):
        self.service_name = service_name
        self.metrics = LatencyMetrics()
        self.memory_metrics = MemoryMetrics()
        self.request_metrics: Dict[str, RequestMetrics] = {}
        self.lock = threading.Lock()
        
        # Start background collection
        self.collection_thread = threading.Thread(
            target=self.run_background_collection,
            daemon=True
        )
        self.collection_thread.start()
        
        # Initialize memory tracking
        self._setup_memory_tracking()
        
    def _setup_memory_tracking(self):
        """Configure memory monitoring"""
        tracemalloc.start()
        self.memory_snapshot = tracemalloc.take_snapshot()
        
        # Track Python object allocations
        self.tracked_objects = set()
        
    def track_request(self, request_id: str) -> RequestMetrics:
        """Track a new request"""
        with self.lock:
            if request_id in self.request_metrics:
                return self.request_metrics[request_id]
            
            metrics = RequestMetrics(request_id=request_id)
            self.request_metrics[request_id] = metrics
            return metrics
        
    def record_latency(self, metrics: LatencyMetrics):
        """Record latency metrics"""
        with self.lock:
            self.metrics = metrics
        
    def record_memory(self, metrics: MemoryMetrics):
        """Record memory metrics"""
        with self.lock:
            self.memory_metrics = metrics
        
    def get_request_metrics(self, request_id: str) -> Optional[RequestMetrics]:
        """Retrieve metrics for a specific request"""
        with self.lock:
            return self.request_metrics.get(request_id)
        
    def list_all_requests(self) -> List[RequestMetrics]:
        """List all tracked requests"""
        with self.lock:
            return list(self.request_metrics.values())
        
    def run_background_collection(self):
        """Run periodic metrics collection"""
        while True:
            try:
                self.collect_metrics()
                time.sleep(1)
            except Exception as e:
                print(f"Metrics collection error: {str(e)}")
                time.sleep(5)

    def collect_metrics(self):
        """Collect and aggregate metrics"""
        # Collect latency metrics
        self.collect_latency_metrics()
        
        # Collect memory metrics
        self.collect_memory_metrics()
        
        # Prune old request metrics
        self.prune_request_metrics()
        
    def collect_latency_metrics(self):
        """Aggregate latency statistics"""
        request_times = []
        
        with self.lock:
            for req_metrics in self.request_metrics.values():
                if req_metrics.end_time:
                    duration = (req_metrics.end_time - req_metrics.start_time).total_seconds()
                    request_times.append(duration)
        
        if request_times:
            request_times.sort()
            
            self.metrics.p50_latency = self.calculate_percentile(request_times, 0.5)
            self.metrics.p95_latency = self.calculate_percentile(request_times, 0.95)
            self.metrics.p99_latency = self.calculate_percentile(request_times, 0.99)
            
            self.metrics.request_rate = len(request_times) / max(1, self.metrics.total_inference_latency) if self.metrics.total_inference_latency > 0 else 0
        
    def calculate_percentile(self, values: List[float], percentile: float) -> float:
        """Calculate the specified percentile"""
        n = len(values)
        if n == 0:
            return 0.0
        
        k = (n - 1) * percentile + 1
        index = int(k)
        
        if index >= n:
            return values[-1]
        
        return values[index]

    def collect_memory_metrics(self):
        """Collect memory usage statistics"""
        # Get virtual memory usage
        mem_info = psutil.virtual_memory()
        
        self.memory_metrics.current_memory = mem_info.used
        self.memory_metrics.peak_memory = max(self.memory_metrics.peak_memory, mem_info.used)
        
        # Get swap memory
        swap_info = psutil.swap_memory()
        self.memory_metrics.swapped_out = swap_info.used
        
        # Take memory snapshot
        snapshot = tracemalloc.take_snapshot()
        
        # Analyze memory usage
        self.analyze_memory_growth(snapshot)
        
    def analyze_memory_growth(self, snapshot):
        """Analyze memory allocation growth"""
        # Compare with previous snapshot
        comparing = snapshot.compare_to(self.memory_snapshot, 'lineno')
        
        # Track allocations
        for diff in comparing:
            if diff.size_diff > 0:
                self.memory_metrics.allocations += diff.size_diff
            elif diff.size_diff < 0:
                self.memory_metrics.deallocations += abs(diff.size_diff)
        
        # Update snapshot
        self.memory_snapshot = snapshot

    def prune_request_metrics(self):
        """Prune completed request metrics to prevent memory overload"""
        # Keep only active requests
        active_requests = {}
        
        with self.lock:
            for req_id, req_metrics in self.request_metrics.items():
                if req_metrics.status == "completed":
                    # Log metrics for completed request
                    self.log_request_metrics(req_metrics)
                else:
                    active_requests[req_id] = req_metrics
                
            self.request_metrics = active_requests

    def log_request_metrics(self, req_metrics: RequestMetrics):
        """Log metrics for a completed request"""
        # Implementation for logging metrics
        pass

# Example usage
if __name__ == "__main__":
    metrics_service = MetricsService()

    # Example request tracking
    request_id = "req_12345"
    request_metrics = metrics_service.track_request(request_id)

    # Simulate inference
    start_inference = time.time()
    # ... inference code ...
    end_inference = time.time()

    # Record metrics
    request_metrics.inference_latency = end_inference - start_inference
    request_metrics.record_end()
    
    # Print metrics
    print(f"Request {request_id} metrics:")
    print(f"  Inference latency: {request_metrics.inference_latency:.3f} seconds")
    print(f"  Input tokens: {request_metrics.input_tokens}")
    print(f"  Output tokens: {request_metrics.output_tokens}")