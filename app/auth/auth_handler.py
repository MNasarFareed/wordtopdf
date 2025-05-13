from fastapi import Header, HTTPException
from app.core.config import API_KEY


def verify_api_key(api_key: str = Header(None)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403,
                            detail={"success": False, "error": "Unauthorized access. Invalid API key."}
)