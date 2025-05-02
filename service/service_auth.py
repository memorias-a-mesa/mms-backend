

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from config.token_utils import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if "error" in payload:
        raise HTTPException(status_code=403, detail="Not authorized")
    return payload