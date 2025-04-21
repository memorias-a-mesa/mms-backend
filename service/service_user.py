from fastapi import HTTPException
from config.database import user_collection

async def check_user_register(user):
    try:
        existing_user = await user_collection.find_one({
            "$or": [
                {"username": user["username"]},
                {"email": user["email"]}
            ]
        })
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking user: {e}")