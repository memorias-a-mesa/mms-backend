from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from config.token_utils import verify_access_token
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

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: LoginRequest, service: LoginService = Depends(get_login_service)):
    return await service.login(request.email, request.password)

@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}