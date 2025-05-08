"""
Serviços de Gerenciamento de Receitas
------------------------------------
"""

from typing import List
from fastapi import HTTPException
from models.receita import Receita, Preparo
from repositories.repository_receita import IReceitaRepository

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
            recipe_data["autorId"] = username
            recipe = await self.repository.create_recipe(recipe_data)
            return Receita(**recipe)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar receita: {str(e)}")

