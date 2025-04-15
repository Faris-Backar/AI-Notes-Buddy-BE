from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

# Simple in-memory cache for UIDs
# In production, use Redis or another distributed cache
uid_cache: Dict[str, dict] = {}

# Model for login request
class LoginRequest(BaseModel):
    uid: str  # UID received from frontend

# Model for login response
class LoginResponse(BaseModel):
    uid: str
    success: bool

# Create router
router = APIRouter(tags=["authentication"])

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Simple login endpoint that stores the UID from the frontend
    without verification
    """
    try:
        uid = request.uid
        
        if not uid:
            raise HTTPException(status_code=400, detail="UID is required")
        
        # Store in cache for future reference
        # You can add more fields if needed
        uid_cache[uid] = {}
        
        return LoginResponse(
            uid=uid,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")