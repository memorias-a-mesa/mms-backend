from pydantic import BaseModel
from typing import Dict, List, Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    myRecipes: List[int] = []  # Lista de IDs das receitas criadas pelo usuário
    favRecipesID: List[int] = []  # Lista de IDs das receitas favoritas

class LoginRequest(BaseModel):
    email: str
    password: str
