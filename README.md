# Simple UID Storage API

A simple FastAPI backend that stores UIDs sent from the frontend.

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the API:
```
python main.py
```

## API Endpoints

### Authentication

- `POST /login` - Simple storage endpoint
  - Body: `{ "uid": "<user-id>" }`
  - Returns: `{ "uid": "<user-id>", "success": true }`
  - Stores the UID in a server-side cache for future reference

### Other

- `GET /` - Welcome message
- `GET /health` - Health check

## Frontend Integration

When a user completes Firebase authentication on your frontend, send the UID to your backend:

```javascript
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";

// Firebase config from console
const firebaseConfig = {
  apiKey: "...",
  authDomain: "...",
  projectId: "...",
  // ...other config
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Example with Google provider
async function loginWithGoogle() {
  const provider = new GoogleAuthProvider();
  
  try {
    // Sign in with Firebase
    const result = await signInWithPopup(auth, provider);
    
    // Get the UID
    const uid = result.user.uid;
    
    // Send UID to your backend
    const response = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ uid: uid }),
    });
    
    const data = await response.json();
    console.log('Login successful, UID stored:', data.uid);
    
    return data;
  } catch (error) {
    console.error('Login failed:', error);
  }
}
```

## Important Security Note

This API does not verify that the UID actually comes from Firebase. In a production environment, you should verify the authentication token instead of accepting UIDs directly. 