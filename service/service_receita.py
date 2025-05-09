"""
Serviços de Gerenciamento de Receitas
------------------------------------
"""

from typing import List
from fastapi import HTTPException
from models.receita import Receita, Preparo
from repositories.repository_receita import IReceitaRepository
from repositories.repository_user import IUserRepository

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
    def __init__(self, repository: IReceitaRepository, validation_service: ReceitaValidationService, user_repository: IUserRepository = None):
        self.repository = repository
        self.validation_service = validation_service
        self.user_repository = user_repository

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

            # Adiciona o ID da receita à lista de receitas do usuário
            if self.user_repository:
                await self.user_repository.add_my_recipe(username, recipe_data["id"])
            
            return Receita(**recipe)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar receita: {str(e)}")

