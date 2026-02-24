from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import logging
from datetime import datetime
import json
from src.analysis_session import AnalysisSession
from src.intent_api import model as intent_model
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Analysis API", description="API for interaction analysis")

# Store sessions in memory (in production, use a database)
sessions: Dict[str, AnalysisSession] = {}

# In a real application, we would use a proper database
# This is a simple in-memory storage

@app.post("/sessions", response_model=Dict[str, Any])
def create_session(user_id: str) -> Dict[str, Any]:
    session_id = f"session_{datetime.now().timestamp():.0f}_{user_id[:3]}"
    
    session = AnalysisSession(
        session_id=session_id,
        user_id=user_id,
        timestamp=datetime.now()
    )
    
    sessions[session_id] = session
    
    return {
        "session_id": session_id,
        "message": "Session created successfully"
    }

@app.get("/sessions/{session_id}", response_model=Dict[str, Any])
def get_session(session_id: str) -> Dict[str, Any]:
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session.to_dict()

@app.post("/sessions/{session_id}/interactions", response_model=Dict[str, Any])
def add_interaction(
    session_id: str,
    interaction: Dict[str, Any]
) -> Dict[str, Any]:
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Validate interaction
    required_fields = ['type', 'content', 'timestamp']
    if not all(field in interaction for field in required_fields):
        raise HTTPException(
            status_code=400,
            detail="Interaction must have type, content, and timestamp"
        )
    
    session.add_interaction(interaction)
    
    return {
        "session_id": session_id,
        "message": "Interaction added successfully",
        "interaction_count": len(session.interactions)
    }

@app.post("/sessions/{session_id}/analyze", response_model=Dict[str, Any])
def analyze_session(session_id: str) -> Dict[str, Any]:
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    analysis_result = session.analyze()
    
    return {
        "session_id": session_id,
        "analysis": analysis_result
    }

@app.delete("/sessions/{session_id}", response_model=Dict[str, Any])
def delete_session(session_id: str) -> Dict[str, Any]:
    session = sessions.pop(session_id, None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "message": "Session deleted successfully"
    }

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Analysis API",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)