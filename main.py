from fastapi import FastAPI
from routers.router_receita import router as receitas
from routers.router_user import router as users
from routers.router_login import router as login_router
from models.receita import Receita
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="memorias-a-mesa")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens. Substitua por uma lista específica em produção.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

app.include_router(receitas)
app.include_router(users)
app.include_router(login_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)