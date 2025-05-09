from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from models.receita import Receita
from service.service_auth import get_current_user
from repositories.repository_receita import ReceitaRepositoryMongo
from repositories.repository_user import UserRepositoryMongo
from service.service_receita import ReceitaService, ReceitaValidationService

router = APIRouter(prefix="/receitas", tags=["Receitas"])

# Dependency Injection
def get_receita_service():
    repository = ReceitaRepositoryMongo()
    user_repository = UserRepositoryMongo()
    validation_service = ReceitaValidationService()
    return ReceitaService(repository, validation_service, user_repository)

@router.get("", response_model=List[Receita])
async def get_recipes(
    service: ReceitaService = Depends(get_receita_service)
):
    """Busca todas as receitas"""
    return await service.get_recipes()

@router.post("", response_model=Receita, status_code=201)
async def create_recipe(
    recipe: Receita,
    current_user: dict = Depends(get_current_user),
    service: ReceitaService = Depends(get_receita_service)
):
    """Cria uma nova receita"""
    return await service.create_recipe(recipe.model_dump(), current_user["sub"])

