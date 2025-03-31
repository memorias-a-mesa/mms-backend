from typing import List
from models.receita import Receita
from repositories.repository_receita import fetch_all_recipes

async def get_all_recipes() -> List[Receita]:
    try:
        recipes = await fetch_all_recipes()
        if recipes:
            return [Receita(**recipe) for recipe in recipes]
        else:
            return []
    except Exception as e:
        raise e