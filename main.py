from fastapi import FastAPI
from .metrics import metrics_service
from .routes import metrics_router

app = FastAPI(
    title="Metrics API",
    description="API for monitoring inference performance metrics",
    version="1.0.0"
)

app.include_router(metrics_router)

@app.on_config_update
async def on_config_update(config):
    """Handle configuration updates"""
    metrics_service.configure(config.metrics)

@app.on_health_check
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}