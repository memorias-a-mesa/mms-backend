from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.receita import Receita
from service.service_auth import get_current_user
from repositories.repository_receita import ReceitaRepositoryMongo
from service.service_receita import ReceitaService, ReceitaValidationService
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/receitas", tags=["Receitas"])

def get_receita_service():
    repository = ReceitaRepositoryMongo()
    validation_service = ReceitaValidationService()
    return ReceitaService(repository, validation_service)

@router.get("", response_model=List[Receita], status_code=200)
async def get_recipes(
    service: ReceitaService = Depends(get_receita_service)
):
    """Busca todas as receitas"""
    try:
        recipes = await service.get_recipes()
        return recipes
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=Receita, status_code=201)
async def create_recipe(
    recipe: Receita,
    current_user: dict = Depends(get_current_user),
    service: ReceitaService = Depends(get_receita_service)
):
    """Cria uma nova receita"""
    try:
        created_recipe = await service.create_recipe(recipe.model_dump(), current_user["sub"])
        return JSONResponse(status_code=200, content=created_recipe.model_dump())
    except HTTPException as he:
        return he
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.post("/{recipe_id}/favorite", status_code=200)
async def favorite_recipe(recipe_id: int,current_user: dict = Depends(get_current_user),service: ReceitaService = Depends(get_receita_service)):
    """Adiciona uma receita aos favoritos do usuário"""
    try:
        result = await service.add_favorite_recipe(recipe_id, current_user["sub"])
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.delete("/{recipe_id}/favorite", status_code=200)
async def unfavorite_recipe(
    recipe_id: int,
    current_user: dict = Depends(get_current_user),
    service: ReceitaService = Depends(get_receita_service)
):
    """Remove uma receita dos favoritos do usuário"""
    try:
        result = await service.remove_favorite_recipe(recipe_id, current_user["sub"])
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.get("/autor/{username}", response_model=List[Receita], status_code=200)
async def get_recipes_by_author(
    username: str,
    service: ReceitaService = Depends(get_receita_service)
):
    """Busca todas as receitas de um autor"""
    try:
        recipes = await service.get_recipes_by_author(username)
        return recipes
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.get("/user/{username}/data", status_code=200)
async def get_user_recipes_summary(
    username: str,
    current_user: dict = Depends(get_current_user),
    service: ReceitaService = Depends(get_receita_service)
):
    """Retorna um resumo das receitas do usuário (criadas e favoritadas)"""
    try:
        # Verifica se o usuário está acessando suas próprias receitas
        if username != current_user["sub"]:
            return HTTPException(status_code=403,
                detail="Você só pode acessar o resumo das suas próprias receitas"
            )
        return await service.get_user_recipes_summary(username)
    except HTTPException as he:
        return he
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

