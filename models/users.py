from pydantic import BaseModel
from typing import Dict, List, Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str
