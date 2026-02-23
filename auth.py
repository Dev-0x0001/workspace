from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import jwt
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_string=False)

@dataclass
class JWTToken:
    """JWT Token structure"""
    payload: Dict[str, Any]
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: datetime = field(default_factory=datetime.now)

class AuthManager:
    """Handles authentication and token management"""
    
    def __init__(
        self,
        secret_key: str = "super-secret-key",
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire = timedelta(minutes=access_token_expire_minutes)
        self.refresh_token_expire = timedelta(days=refresh_token_expire_days)
        
    def create_access_token(self, data: Dict[str, Any]) -> JWTToken:
        """Create a new access token"""
        expires = datetime.utcnow() + self.access_token_expire
        payload = data.copy()
        payload.update({'exp': expires})
        
        access_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        return JWTToken(
            payload=payload,
            access_token=access_token,
            expires_at=expires
        )

    def create_refresh_token(self, data: Dict[str, Any]) -> JWTToken:
        """Create a new refresh token"""
        expires = datetime.utcnow() + self.refresh_token_expire
        payload = data.copy()
        payload.update({'exp': expires})
        
        refresh_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        return JWTToken(
            payload=payload,
            access_token=refresh_token,
            expires_at=expires
        )

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            logger.error("Invalid token")
            return None