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
