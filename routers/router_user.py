from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from models.users import UserCreate, UserData
from service.service_user import UserService, UserValidationService
from repositories.repository_user import UserRepositoryMongo
from repositories.repository_receita import ReceitaRepositoryMongo
from service.service_auth import get_current_user
from config.database import recipes_collection

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

@router.post("/favorite/{recipe_id}")
async def add_favorite_recipe(
    recipe_id: int,
    current_user: dict = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    """Adiciona uma receita aos favoritos do usuário"""
    try:
        receita_repository = ReceitaRepositoryMongo()
        result = await service.add_favorite_recipe(
            current_user["sub"], 
            recipe_id, 
            recipes_collection,
            receita_repository
        )
        return JSONResponse(
            status_code=200,
            content=result
        )
    except HTTPException as e:
        raise e

@router.delete("/favorite/{recipe_id}")
async def remove_favorite_recipe(
    recipe_id: int,
    current_user: dict = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    """Remove uma receita dos favoritos do usuário"""
    try:
        receita_repository = ReceitaRepositoryMongo()
        result = await service.remove_favorite_recipe(
            current_user["sub"], 
            recipe_id,
            receita_repository
        )
        return JSONResponse(
            status_code=200,
            content=result
        )
    except HTTPException as e:
        raise e

@router.get("/data", response_model=UserData)
async def get_user_data(
    current_user: dict = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    """Retorna os dados do usuário autenticado"""
    return await service.get_user_data(current_user["sub"])
