from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from models.users import UserCreate, UserData
from service.service_user import UserService, UserValidationService
from repositories.repository_user import UserRepositoryMongo
from service.service_auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

def get_user_service():
    repository = UserRepositoryMongo()
    validation_service = UserValidationService()
    return UserService(repository, validation_service)

@router.post("", status_code=201)
async def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    try:
        result = await service.create_user(user)
        if result != []:
            return JSONResponse(
                status_code=201,
                content={"detail": "User created successfully"}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"detail": "User already exists"}
            )
    except HTTPException as he:
        return he
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.get("/data", response_model=UserData, status_code=200)
async def get_user_data(
    current_user: dict = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    """Retorna os dados do usuário autenticado"""
    try:
        user_data = await service.get_user_data(current_user["sub"])
        return user_data
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
