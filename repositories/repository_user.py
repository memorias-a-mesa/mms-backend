from config.database import recipes_collection, user_collection
from models.receita import Receita
from typing import List

async def create_new_user(user_data: dict):
    try:
        result = await user_collection.insert_one(user_data)
        return {"message": "Usuário criado com sucesso"}
    except Exception as e:
        raise Exception(f"Erro ao criar novo usuário: {e}")
