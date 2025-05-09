from abc import ABC, abstractmethod
from config.database import recipes_collection, user_collection
from models.receita import Receita
from typing import List
from models.users import UserCreate

class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user_data: dict):
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str):
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str):
        pass

    @abstractmethod
    async def add_favorite_recipe(self, username: str, recipe_id: int):
        pass

    @abstractmethod
    async def add_my_recipe(self, username: str, recipe_id: int):
        pass

class UserRepositoryMongo(IUserRepository):
    async def create_user(self, user_data: dict):
        try:
            await user_collection.insert_one(user_data)
            return {"message": "User created successfully"}
        except Exception as e:
            raise Exception(f"Error creating new user: {e}")

    async def get_user_by_email(self, email: str):
        try:
            return await user_collection.find_one({"email": email})
        except Exception as e:
            raise Exception(f"Error finding user by email: {e}")

    async def get_user_by_username(self, username: str):
        try:
            return await user_collection.find_one({"username": username})
        except Exception as e:
            raise Exception(f"Error finding user by username: {e}")

    async def add_favorite_recipe(self, username: str, recipe_id: int):
        try:
            result = await user_collection.update_one(
                {"username": username},
                {"$addToSet": {"favRecipesID": recipe_id}}  # Using addToSet to avoid duplicates
            )
            if result.modified_count == 0:
                raise Exception("User not found or recipe already in favorites")
            return {"message": "Recipe added to favorites successfully"}
        except Exception as e:
            raise Exception(f"Error adding favorite recipe: {e}")

    async def add_my_recipe(self, username: str, recipe_id: int):
        try:
            result = await user_collection.update_one(
                {"username": username},
                {"$addToSet": {"myRecipes": recipe_id}}
            )
            if result.modified_count == 0:
                raise Exception("User not found or error adding recipe")
            return {"message": "Recipe added to user's recipes successfully"}
        except Exception as e:
            raise Exception(f"Error adding recipe to user's recipes: {e}")
