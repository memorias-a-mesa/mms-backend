from config.database import recipes_collection
from models.receita import Receita
from typing import List

async def fetch_all_recipes():
    try:
        recipes_cursor = recipes_collection.find({}, {"_id": 0})
        recipes = await recipes_cursor.to_list(100) 
        return recipes
    except Exception as e:
        raise Exception(f"Erro ao buscar receitas: {e}")