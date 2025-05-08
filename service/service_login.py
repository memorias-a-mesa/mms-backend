"""
Serviço de Login
--------------
"""

import bcrypt
from repositories.repository_login import ILoginRepository
from bson import ObjectId
from config.token_utils import create_access_token

# Login Service
# This class handles the business logic for user login.
class LoginService:
    def __init__(self, repository: ILoginRepository):
        self.repository = repository

    async def login(self, email: str, password: str):
        user = await self.repository.get_user_by_email(email)
        if not user:
            return {"error": "Invalid credentials"}

        # Verify password using bcrypt directly
        password_match = bcrypt.checkpw(
            password.encode('utf-8'),
            user["password"].encode('utf-8')
        )
        
        if not password_match:
            return {"error": "Invalid credentials"}

        # Generate a JWT token for the user
        token_data = {"sub": user.get("username", "Unknown")}
        access_token = create_access_token(data=token_data)

        return {"message": "Login successful", "access_token": access_token}