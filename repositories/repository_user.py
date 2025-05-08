from abc import ABC, abstractmethod
from config.database import recipes_collection, user_collection
from models.receita import Receita
from typing import List
from models.users import UserCreate

class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user_data: dict):
        pass

class UserRepositoryMongo(IUserRepository):
    async def create_user(self, user_data: dict):
        try:
            await user_collection.insert_one(user_data)
            return {"message": "User created successfully"}
        except Exception as e:
            raise Exception(f"Error creating new user: {e}")
