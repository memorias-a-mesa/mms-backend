from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from models.users import UserCreate
from service.service_user import UserService, UserValidationService
from repositories.repository_user import UserRepositoryMongo

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
        return JSONResponse(
            status_code=201,
            content={"detail": "User created successfully"}
        )
    except HTTPException as e:
        raise e
