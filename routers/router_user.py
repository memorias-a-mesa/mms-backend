from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from bson.objectid import ObjectId

from models.users import UserCreate
from repositories.repository_user import create_new_user
from service.service_user import check_user_register, manage_user_registration
import bcrypt

router = APIRouter()

@router.post("/users")
async def create_user(user: UserCreate):
    try: 
        new_user = {
            "username": user.username,
            "email": user.email,
            "password": user.password,
        }
        await manage_user_registration(new_user)
        return JSONResponse(status_code=201, content={"detail": "User created successfully"})
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
