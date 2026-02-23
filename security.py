from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from .deps import get_api_key

# Security
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_string=False)

async def get_current_user(api_key: str = Depends(APIKeyHeader(name="X-API-Key"))):
    """Get authenticated user"""
    # In a real system, this would look up the user
    if api_key == "valid_api_key":
        return "admin"
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key"
    )