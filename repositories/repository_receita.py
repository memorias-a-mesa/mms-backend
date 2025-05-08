from abc import ABC, abstractmethod
from config.database import recipes_collection
from models.receita import Receita
from typing import List, Optional

class IReceitaRepository(ABC):
    @abstractmethod
    async def get_all_recipes(self) -> List[dict]:
        """Busca todas as receitas"""
        pass

    @abstractmethod
    async def create_recipe(self, recipe: dict) -> dict:
        """Cria uma nova receita"""
        pass

class ReceitaRepositoryMongo(IReceitaRepository):
    async def get_all_recipes(self) -> List[dict]:
        try:
            return await recipes_collection.find({}, {"_id": 0}).to_list(length=100)
        except Exception as e:
            raise Exception(f"Erro ao buscar receitas: {e}")

    async def create_recipe(self, recipe: dict) -> dict:
        try:
            await recipes_collection.insert_one(recipe)
            return recipe
        except Exception as e:
            raise Exception(f"Erro ao criar receita: {e}")

