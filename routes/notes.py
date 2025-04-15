from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import logging
from models.notesModel import NoteCreate, NoteResponse, NoteUpdate
from services import firebase_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for notes as fallback
notes_db: Dict[str, dict] = {}

# Create router
router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

@router.post("/create", response_model=NoteResponse)
async def create_note(note: NoteCreate):
    try:
        note_id = str(uuid.uuid4())
        current_time = datetime.now()
        
        note_data = {
            "id": note_id,
            "userUid": note.userUid,
            "title": note.title,
            "content": note.content,
            "createUserName": note.createUserName,
            "isActive": note.isActive,
            "status": note.status,
            "createdDate": current_time,
            "modifiedDate": current_time
        }
        
        # Log the note data being saved
        logger.info(f"Saving note data: {note_data}")
        
        # Store in memory database (fallback)
        notes_db[note_id] = note_data
        
        # Save to Firebase
        firebase_service.save_note_to_firebase(note_data)
        
        return note_data
    except Exception as e:
        logger.error(f"Error creating note: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/get-all", response_model=List[NoteResponse])
async def get_notes(user_uid: str):
    try:
        firebase_notes = firebase_service.get_user_notes_from_firebase(user_uid)
        if firebase_notes:
            return firebase_notes
        
        user_notes = [
            note for note in notes_db.values() 
            if note["userUid"] == user_uid
        ]
        
        return user_notes
    except Exception as e:
        logger.error(f"Error getting notes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-by-id/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str):

    try:
        firebase_note = firebase_service.get_note_from_firebase(note_id)
        if firebase_note:
            return firebase_note
        
        if note_id not in notes_db:
            raise HTTPException(status_code=404, detail="Note not found")
        
        return notes_db[note_id]
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error getting note: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{note_id}", response_model=NoteResponse)
async def update_note(note_id: str, note_update: NoteUpdate):

    try:
        firebase_note = firebase_service.get_note_from_firebase(note_id)
        if firebase_note:
            note = firebase_note
        else:
            if note_id not in notes_db:
                raise HTTPException(status_code=404, detail="Note not found")
            note = notes_db[note_id]
        
        update_data = {}
        if note_update.title is not None:
            note["title"] = note_update.title
            update_data["title"] = note_update.title
        if note_update.content is not None:
            note["content"] = note_update.content
            update_data["content"] = note_update.content
        if note_update.isActive is not None:
            note["isActive"] = note_update.isActive
            update_data["isActive"] = note_update.isActive
        if note_update.status is not None:
            note["status"] = note_update.status
            update_data["status"] = note_update.status
        
        current_time = datetime.now()
        note["modifiedDate"] = current_time
        update_data["modifiedDate"] = current_time
        
        notes_db[note_id] = note
        
        # Update in Firebase with only changed fields
        firebase_service.update_note_in_firebase(note_id, update_data)
        
        return note
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating note: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{note_id}")
async def delete_note(note_id: str):
    try:
        logger.info(f"Attempting to delete note with ID: {note_id}")
        
        firebase_note = firebase_service.get_note_from_firebase(note_id)
        logger.info(f"Firebase note check result: {'Found' if firebase_note else 'Not found'}")
        
        if not firebase_note and note_id not in notes_db:
            logger.error(f"Note not found in either Firebase or local DB: {note_id}")
            raise HTTPException(status_code=404, detail="Note not found")
        
        if note_id in notes_db:
            del notes_db[note_id]
            logger.info(f"Deleted note from local DB: {note_id}")
        
        delete_result = firebase_service.delete_note_from_firebase(note_id)
        logger.info(f"Firebase delete result: {'Success' if delete_result else 'Failed'}")
        
        return {"message": "Note deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting note: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 