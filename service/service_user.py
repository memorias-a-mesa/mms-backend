from fastapi import HTTPException
import re
import bcrypt
from models.users import UserCreate
from repositories.repository_user import IUserRepository

class UserValidationService:
    @staticmethod
    async def validate_email(email: str) -> bool:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|outlook\.com)$'
        if not re.match(email_pattern, email):
            raise HTTPException(status_code=400, detail="Invalid email: must be Gmail or Outlook.")
        return True

    @staticmethod
    def validate_password(password: str) -> bool:
        password_pattern = r'^(?=.*[A-Z]).{8,}$'
        if not re.match(password_pattern, password):
            raise HTTPException(
                status_code=400, 
                detail="Password must have at least 8 characters and one uppercase letter."
            )
        return True

class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

class UserService:
    def __init__(self, repository: IUserRepository, validation_service: UserValidationService):
        self.repository = repository
        self.validation_service = validation_service
        self.password_service = PasswordService()

    async def create_user(self, user_data: UserCreate):
        user_valid = False
        """Cria um novo usuário"""
        try:
            # Verifica se o email já existe
            existing_user = await self.repository.get_user_by_email(user_data.email)
            if existing_user:
               user_valid = True

            # Verifica se o username já existe
            existing_user = await self.repository.get_user_by_username(user_data.username)
            if existing_user:
                 user_valid = True

            # Hash da senha
            hashed_password = self.password_service.hash_password(user_data.password)
              # Prepara os dados do usuário
            user_dict = {
                "username": user_data.username,
                "email": user_data.email,
                "password": hashed_password
            }
            if user_valid == False:
                return await self.repository.create_user(user_dict)
            if user_valid == True:
                return []
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_user_data(self, username: str):
        """Retorna os dados do usuário"""
        try:
            return await self.repository.get_user_data(username)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
