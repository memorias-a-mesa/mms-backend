from fastapi import HTTPException
import re
from config.database import user_collection

async def check_user_register(user):
    try:
        # Validate email format and domain
        email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|outlook\.com)$'
        if not re.match(email_pattern, user["email"]):
            raise HTTPException(status_code=400, detail="Insira um e-mail válido: Gmail ou Outlook.")

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
    
async def manage_user_registration(user_data):
    try:
        # Check if the user can be registered
        await check_user_register(user_data)
        
        # If user can be registered, insert the user into the database
        await user_collection.insert_one(user_data)
        return {"message": "User registered successfully"}
    except HTTPException as e:
        raise e
