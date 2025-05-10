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

    @abstractmethod
    async def get_max_recipe_id(self) -> int:
        """Busca o maior ID atual das receitas"""
        pass

    @abstractmethod
    async def increment_recipe_rating(self, recipe_id: int) -> bool:
        """Incrementa a quantidade de avaliações de uma receita"""
        pass

    @abstractmethod
    async def decrement_recipe_rating(self, recipe_id: int) -> bool:
        """Decrementa a quantidade de avaliações de uma receita"""
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

    async def get_max_recipe_id(self) -> int:
        try:
            result = await recipes_collection.find_one(
                filter={},
                sort=[("id", -1)],
                projection={"id": 1}
            )
            return result["id"] if result and "id" in result else 0
        except Exception as e:
            raise Exception(f"Erro ao buscar maior ID de receita: {e}")

    async def increment_recipe_rating(self, recipe_id: int) -> bool:
        try:
            result = await recipes_collection.update_one(
                {"id": recipe_id},
                {"$inc": {"qtdAvaliacao": 1}}
            )
            if result.modified_count == 0:
                raise Exception("Recipe not found")
            return True
        except Exception as e:
            raise Exception(f"Error incrementing recipe rating: {e}")

    async def decrement_recipe_rating(self, recipe_id: int) -> bool:
        try:
            # Verificamos se a receita existe e tem qtdAvaliacao > 0
            recipe = await recipes_collection.find_one({"id": recipe_id})
            if not recipe:
                raise Exception("Recipe not found")
            if recipe.get("qtdAvaliacao", 0) <= 0:
                raise Exception("Rating count already at zero")

            result = await recipes_collection.update_one(
                {"id": recipe_id},
                {"$inc": {"qtdAvaliacao": -1}}
            )
            if result.modified_count == 0:
                raise Exception("Failed to update recipe rating")
            return True
        except Exception as e:
            raise Exception(f"Error decrementing recipe rating: {e}")

