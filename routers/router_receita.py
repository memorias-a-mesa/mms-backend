from fastapi import APIRouter, HTTPException, status
from typing import List
from models.receita import Receita
from service.service_receita import get_all_recipes

router = APIRouter(prefix="/receitas", tags=["Receitas"])

@router.get("", response_model=List[Receita]) 
async def retrieve_recipes():
    try:
        recipes = await get_all_recipes()
        if recipes != []:
            return recipes
        raise HTTPException(status_code=404, detail="No recipes found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")