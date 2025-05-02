from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from models.receita import Receita
from service.service_auth import get_current_user
from service.service_receita import get_all_recipes
from config.token_utils import verify_access_token

router = APIRouter(prefix="/receitas", tags=["Receitas"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.get("", response_model=List[Receita]) 
async def retrieve_recipes(current_user: dict = Depends(get_current_user)):
    try:
        recipes = await get_all_recipes()
        if recipes != []:
            return recipes
        raise HTTPException(status_code=404, detail="No recipes found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")