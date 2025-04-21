from fastapi import HTTPException
import re
from config.database import user_collection
from models.users import UserCreate
from repositories.repository_user import create_new_user
import bcrypt

async def check_user_register(user):
    try:
        # Validate email format and domain
        email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|outlook\.com)$'
        if not re.match(email_pattern, user["email"]):
            raise HTTPException(status_code=400, detail="Insira um e-mail válido: Gmail ou Outlook.")

        # Validate password 
        password_pattern = r'^(?=.*[A-Z]).{8,}$'
        if not re.match(password_pattern, user["password"]):
            raise HTTPException(status_code=400, detail="A senha deve ter no mínimo 8 caracteres e pelo menos uma letra maiúscula.")

        # Validate if user is already registered
        existing_user = await user_collection.find_one({
            "$or": [
                {"username": user["username"]},
                {"email": user["email"]}
            ]
        })
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists")
        
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking user: {e}")
    
def manage_password(user):
    user: UserCreate = UserCreate.model_validate(user)
    password = user.password.encode('utf-8')
    hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hash_password.decode('utf-8'),
    }  
    return new_user  
    
async def manage_user_registration(user_data):
    try:
        # Check if the user can be registered
        await check_user_register(user_data)
        
        # If user can be registered, insert the user into the database
        user = manage_password(user_data)
        await create_new_user(user)
        return {"message": "User registered successfully"}
    except HTTPException as e:
        raise e
