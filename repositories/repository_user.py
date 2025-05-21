from abc import ABC, abstractmethod
from config.database import user_collection as user_collection
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
    async def get_user_data(self, username: str):
        pass

class UserRepositoryMongo(IUserRepository):
    async def create_user(self, user_data: dict):
        try:
            res = await user_collection.insert_one(user_data)
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

    async def get_user_data(self, username: str):
        try:
            user = await user_collection.find_one(
                {"username": username},
                {"_id": 0, "password": 0}  
            )
            if not user:
                raise Exception("User not found")
            return user
        except Exception as e:
            raise Exception(f"Error retrieving user data: {e}")
