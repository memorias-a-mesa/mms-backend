from fastapi import FastAPI
from routers.router_receita import router as receitas
from models.receita import Receita

app = FastAPI(title="memorias-a-mesa")

app.include_router(receitas)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)