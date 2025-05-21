from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UserData(BaseModel):
    username: str
    email: str
