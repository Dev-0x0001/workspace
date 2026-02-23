from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
from dataclasses import asdict
import json
from datetime import datetime

from .metrics import MetricsService, RequestMetrics, LatencyMetrics

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

metrics_service = MetricsService()

@router.get("/")
async def get_overview():
    """Get metrics overview"""
    try:
        latency = asdict(metrics_service.metrics)
        memory = asdict(metrics_service.memory_metrics)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "latency": latency,
            "memory": memory
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/requests")
async def get_requests(
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    """List recent requests with metrics"""
    try:
        requests = metrics_service.list_all_requests()[skip:skip+limit]
        return [asdict(r) for r in requests]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/requests/{request_id}")
async def get_request(request_id: str):
    """Get metrics for specific request"""
    try:
        metrics = metrics_service.get_request_metrics(request_id)
        if not metrics:
            raise HTTPException(status_code=404, detail="Request not found")
        return asdict(metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/requests")
async def create_request(request_id: str):
    """Track a new request"""
    try:
        metrics = metrics_service.track_request(request_id)
        return asdict(metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/requests/{request_id}/complete")
async def complete_request(request_id: str):
    """Mark request as completed"""
    try:
        metrics = metrics_service.get_request_metrics(request_id)
        if not metrics:
            raise HTTPException(status_code=404, detail="Request not found")
        
        metrics.record_end()
        return {"status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))