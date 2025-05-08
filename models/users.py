from pydantic import BaseModel
from typing import Dict, List, Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    favRecipesID: List[str] = []

class LoginRequest(BaseModel):
    email: str
    password: str
