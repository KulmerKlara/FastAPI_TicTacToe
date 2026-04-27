from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import get_settings

settings = get_settings()
api_key_header = APIKeyHeader(name=settings.api_key_header, auto_error=False)


def get_api_key_user(api_key: str | None = Security(api_key_header)) -> str:
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key")
    username = settings.key_to_user.get(api_key)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return username
