"""
Serviços de Gerenciamento de Receitas
------------------------------------
"""

from typing import List
from fastapi import HTTPException
from models.receita import Receita, Preparo
from repositories.repository_receita import IReceitaRepository
from repositories.repository_receita import ReceitaRepositoryMongo

async def get_fav_recipes_for_the_week() -> List[dict]:
    try:
        repository = ReceitaRepositoryMongo()
        recipes = await repository.get_most_favorited_recipes()
        return recipes if recipes else []
    except Exception as e:
        print(f"Error getting favorite recipes: {str(e)}")
        return []

class ReceitaValidationService:
    @staticmethod
    def validate_recipe_data(recipe_data: dict) -> bool:
        """Valida os dados da receita"""
        required_fields = ["nomeReceita", "descricaoReceita", "sentimentoReceita", 
                         "preparos", "tempoPreparo", "imagemReceita", "qtdeFinal"]
        
        for field in required_fields:
            if field not in recipe_data:
                raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {field}")
        
        if not isinstance(recipe_data["preparos"], list) or len(recipe_data["preparos"]) == 0:
            raise HTTPException(status_code=400, detail="A receita deve ter pelo menos um preparo")
            
        return True

class ReceitaService:
    def __init__(self, repository: IReceitaRepository, validation_service: ReceitaValidationService):
        self.repository = repository
        self.validation_service = validation_service

    async def get_recipes(self) -> List[Receita]:
        """Busca todas as receitas"""
        try:
            recipes = await self.repository.get_all_recipes()
            return [Receita(**recipe) for recipe in recipes] if recipes else []
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar receitas: {str(e)}")

    async def create_recipe(self, recipe_data: dict, username: str) -> Receita:
        """Cria uma nova receita"""
        try:
            self.validation_service.validate_recipe_data(recipe_data)
            
            # Gera o próximo ID sequencial
            current_max_id = await self.repository.get_max_recipe_id()
            recipe_data["id"] = current_max_id + 1
            
            recipe_data["autorId"] = username
            recipe = await self.repository.create_recipe(recipe_data)
            
            return Receita(**recipe)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar receita: {str(e)}")

    async def add_favorite_recipe(self, recipe_id: int, username: str) -> dict:
        """Adiciona a receita aos favoritos do usuário"""
        try:
            return await self.repository.add_favorite_recipe(recipe_id, username)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def remove_favorite_recipe(self, recipe_id: int, username: str) -> dict:
        """Remove a receita dos favoritos do usuário"""
        try:
            return await self.repository.remove_favorite_recipe(recipe_id, username)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_recipes_by_author(self, username: str) -> List[Receita]:
        """Busca todas as receitas de um autor"""
        try:
            recipes = await self.repository.get_recipes_by_author(username)
            return [Receita(**recipe) for recipe in recipes] if recipes else []
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar receitas do autor: {str(e)}")

    async def get_user_recipes_summary(self, username: str) -> dict:
        """Retorna um resumo das receitas do usuário, incluindo criadas e favoritadas"""
        try:
            # Busca receitas criadas pelo usuário
            created_recipes = await self.repository.get_recipes_by_author(username)
            
            # Busca receitas favoritadas pelo usuário
            favorited_recipes = await self.repository.get_recipes_by_favorite(username)
            
            return {
                "created_recipes": [Receita(**recipe) for recipe in created_recipes] if created_recipes else [],
                "favorited_recipes": [Receita(**recipe) for recipe in favorited_recipes] if favorited_recipes else [],
                "total_created": len(created_recipes),
                "total_favorited": len(favorited_recipes)
            }
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Erro ao buscar resumo das receitas do usuário: {str(e)}"
            )
