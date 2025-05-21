"""
Serviço de Login
--------------
"""

import bcrypt
from fastapi import HTTPException
from repositories.repository_login import ILoginRepository
from bson import ObjectId
from config.token_utils import create_access_token

# Login Service
# This class handles the business logic for user login.
class LoginService:
    def __init__(self, repository: ILoginRepository):
        self.repository = repository

    async def login(self, email: str, password: str):
        try:
            # Get user from repository
            user = await self.repository.get_user_by_email(email)
            
            if not user:
                raise HTTPException(status_code=401, detail="Invalid email or password")

            if not user.get("password"):
                raise HTTPException(status_code=500, detail="User password not found in database")

            # Verify password using bcrypt
            try:
                password_match = bcrypt.checkpw(
                    password.encode('utf-8'),
                    user["password"].encode('utf-8')
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail="Error verifying password")

            if not password_match:
                raise HTTPException(status_code=401, detail="Invalid email or password")

            # Generate JWT token
            token_data = {"sub": user.get("username")}
            if not token_data["sub"]:
                raise HTTPException(status_code=500, detail="Username not found in user data")
                
            access_token = create_access_token(data=token_data)
            
            return {
                "message": "Login successful",
                "access_token": access_token,
                "token_type": "bearer"
            }
            
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))