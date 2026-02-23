from contextlib import contextmanager
import time
import threading
from typing import Optional

from .metrics import metrics_service
from .logging import logger

# Global rate limiter
rate_limiter = {}
lock = threading.Lock()

@contextmanager
def rate_limit(key: str, limit: int, window: int):
    """Rate limiting context manager"""
    global rate_limiter
    
    with lock:
        current = rate_limiter.get(key, [])
        now = time.time()
        
        # Remove old requests outside the window
        current = [t for t in current if now - t < window]
        
        if len(current) >= limit:
            raise Exception(f"Rate limit exceeded for {key}")
        
        current.append(now)
        rate_limiter[key] = current
        
    try:
        yield
    except Exception as e:
        logger.error(f"Rate limit error: {str(e)}")
        raise

@contextmanager
def distributed_lock(lock_key: str):
    """Context manager for distributed locking"""
    lock_acquired = False
    try:
        # Attempt to acquire lock (non-blocking)
        lock_acquired = lock.acquire(timeout=5)
        if not lock_acquired:
            raise Exception(f"Failed to acquire lock: {lock_key}")
        
        yield True
    except Exception as e:
        logger.error(f"Lock error: {str(e)}")
        yield False
    finally:
        if lock_acquired:
            lock.release()