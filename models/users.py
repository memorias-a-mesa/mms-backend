from pydantic import BaseModel
from typing import Dict, List, Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    myRecipes: List[int] = []
    favRecipesID: List[int] = []

class LoginRequest(BaseModel):
    email: str
    password: str

class UserData(BaseModel):
    username: str
    email: str
    myRecipes: List[int]
    favRecipesID: List[int]
