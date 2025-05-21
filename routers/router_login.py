from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from config.token_utils import verify_access_token
from models.users import LoginRequest
from service.service_auth import get_current_user
from service.service_login import LoginService
from repositories.repository_login import UserRepository

# FastAPI Router for Login
# This router handles the API endpoint for user login.
router = APIRouter()

# Dependency Injection Function
# This function provides an instance of LoginService with its dependencies.
def get_login_service():
    repository = UserRepository()  # Concrete implementation of the repository.
    return LoginService(repository)  # Inject the repository into the service.

@router.post("/login", status_code=200)
async def login(request: LoginRequest, service: LoginService = Depends(get_login_service)):
    try:
        result = await service.login(request.email, request.password)
        
        if "error" in result:
            return HTTPException(status_code=401, detail=result["error"])
        return result
    except HTTPException as he:
        return he
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))