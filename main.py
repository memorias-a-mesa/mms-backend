from fastapi import FastAPI
from routers.router_receita import router as receitas
from routers.router_user import router as users
from routers.router_login import router as login_router
from models.receita import Receita
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from service.service_email import SchedulerService, SMTPEmailService, user_service, email_user, email_password, scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting scheduler...")
    # Instanciar dependências
    email_service = SMTPEmailService(email_user=email_user, email_password=email_password)
    scheduler_service = SchedulerService(scheduler=scheduler, email_service=email_service, user_service=user_service)

    # Iniciar o scheduler
    scheduler_service.start_scheduler()
    
    yield
    # Shutdown
    print("API encerrada.")

app = FastAPI(title="memorias-a-mesa", lifespan=lifespan)

origins = [
    "https://memoriasamesa-728b.vercel.app",
    "http://localhost:4200"
]
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",  # Permite todas as origens. Substitua por uma lista específica em produção.
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