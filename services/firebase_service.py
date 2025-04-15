from datetime import datetime
from typing import Dict, Any, Optional
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

firebase_available = False
firestore_db = None
notes_collection = None
auth = None
users_collection = None

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, auth
    
    cred_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ai-notes-buddy-firebase-adminsdk-fbsvc-efdf3046ad.json')
    
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    
    firestore_db = firestore.client()
    notes_collection = firestore_db.collection('notes')
    users_collection = firestore_db.collection('users')
    firebase_available = True
    logger.info("Firebase Firestore initialized successfully")
except Exception as e:
    firebase_available = False
    logger.error(f"Firebase Firestore initialization error: {e}")
    logger.info("Firebase functionality will not be available")

def verify_id_token(token: str) -> Dict[str, Any]:

    try:
        if not firebase_available:
            raise Exception("Firebase is not available")
            
        decoded_token = auth.verify_id_token(token)
        logger.info(f"Token verified successfully for user: {decoded_token.get('uid')}")
        return decoded_token
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise

def is_firebase_available() -> bool:
    return firebase_available

def save_note_to_firebase(note_data: Dict[str, Any]) -> bool:
    if not firebase_available:
        return False
    
    try:
        note_id = note_data["id"]
        
        firestore_data = note_data.copy()
        
        for key, value in firestore_data.items():
            if isinstance(value, datetime):
                firestore_data[key] = value.isoformat()
        
        notes_collection.document(note_id).set(firestore_data)
        print(f"Note {note_id} saved to Firebase")
        return True
    except Exception as e:
        print(f"Error saving note to Firebase: {e}")
        return False

def get_note_from_firebase(note_id: str) -> Optional[Dict[str, Any]]:
    if not firebase_available:
        return None
    
    try:
        doc_ref = notes_collection.document(note_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        else:
            return None
    except Exception as e:
        print(f"Error retrieving note from Firebase: {e}")
        return None

def get_user_notes_from_firebase(user_uid: str) -> list:

    if not firebase_available:
        return []
    
    try:
        query_ref = notes_collection.where("userUid", "==", user_uid)
        docs = query_ref.stream()
        
        notes = []
        for doc in docs:
            notes.append(doc.to_dict())
        
        return notes
    except Exception as e:
        print(f"Error retrieving user notes from Firebase: {e}")
        return []

def update_note_in_firebase(note_id: str, note_data: Dict[str, Any]) -> bool:

    if not firebase_available:
        return False
    
    try:
        firestore_data = note_data.copy()
        
        for key, value in firestore_data.items():
            if isinstance(value, datetime):
                firestore_data[key] = value.isoformat()
        
        notes_collection.document(note_id).update(firestore_data)
        print(f"Note {note_id} updated in Firebase")
        return True
    except Exception as e:
        print(f"Error updating note in Firebase: {e}")
        return False

def delete_note_from_firebase(note_id: str) -> bool:
    
    if not firebase_available:
        return False
    
    try:
        notes_collection.document(note_id).delete()
        print(f"Note {note_id} deleted from Firebase")
        return True
    except Exception as e:
        print(f"Error deleting note from Firebase: {e}")
        return False

def save_user_to_firebase(user_data: Dict[str, Any]) -> bool:
    if not firebase_available:
        return False
    
    try:
        user_id = user_data["uid"]
        
        firestore_data = user_data.copy()
        
        for key, value in firestore_data.items():
            if isinstance(value, datetime):
                firestore_data[key] = value.isoformat()
        
        users_collection.document(user_id).set(firestore_data)
        logger.info(f"User {user_id} saved to Firebase")
        return True
    except Exception as e:
        logger.error(f"Error saving user to Firebase: {e}")
        return False

def get_user_from_firebase(user_id: str) -> Optional[Dict[str, Any]]:
    if not firebase_available:
        return None
    
    try:
        doc_ref = users_collection.document(user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        else:
            return None
    except Exception as e:
        logger.error(f"Error retrieving user from Firebase: {e}")
        return None 