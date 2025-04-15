from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from datetime import datetime
import logging
from models.userModel import UserCreate, UserResponse
from services import firebase_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/create", response_model=UserResponse)
async def create_user(user: UserCreate):
    try:
        current_time = datetime.now()
        
        user_data = {
            "uid": user.uid,
            "email": user.email,
            "displayName": user.displayName,
            "photoURL": user.photoURL,
            "createdDate": current_time,
            "modifiedDate": current_time
        }
        
        # Log the user data being saved
        logger.info(f"Saving user data: {user_data}")
        
        # Save to Firebase
        firebase_service.save_user_to_firebase(user_data)
        
        return user_data
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 