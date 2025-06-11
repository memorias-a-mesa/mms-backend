import os
# Importar AsyncIOScheduler em vez de BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
import asyncio
import smtplib
from email.message import EmailMessage
from service.service_receita import ReceitaService
from service.service_user import UserService
from repositories.repository_user import UserRepositoryMongo
from service.service_user import UserValidationService
from repositories.repository_receita import ReceitaRepositoryMongo
from service.service_receita import ReceitaValidationService, ReceitaService
import logging
from abc import ABC, abstractmethod

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Variáveis de ambiente para o e-mail
email_user = os.getenv("EMAIL")
email_password = os.getenv("SENHAEMAIL")

# Configurar o fuso horário para o Brasil
brasil_timezone = timezone("America/Sao_Paulo")

# Instanciar o scheduler assíncrono
# MUDANÇA CRUCIAL AQUI: Usando AsyncIOScheduler
scheduler = AsyncIOScheduler(timezone=brasil_timezone)

# Instanciar dependências do serviço de usuário
repository = UserRepositoryMongo() 
validation_service = UserValidationService()
user_service = UserService(repository=repository, validation_service=validation_service)

# Instanciar dependências do serviço de receita
repository_receita = ReceitaRepositoryMongo()
validation_service_receita = ReceitaValidationService()
receita_service = ReceitaService(repository_receita, validation_service_receita)

# Interface abstrata para serviços de e-mail, para que qualquer classe filha implemente o método send_email.
class EmailService(ABC):
    @abstractmethod
    def send_email(self, to_address: str, subject: str, body: str):
        pass
    
# Implementação concreta de EmailService usando SMTP
class SMTPEmailService(EmailService):
    def _init_(self, email_user: str, email_password: str, email_host: str = "smtp.gmail.com", email_port: int = 587):
        self.email_user = email_user
        self.email_password = email_password
        self.email_host = email_host
        self.email_port = email_port

    def send_email(self, to_address: str, subject: str, body: str):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.email_user
        msg['To'] = to_address
        msg.add_alternative(body, subtype='html')

        logging.info(f"Enviando e-mail para {to_address} com assunto '{subject}'...")

        try:
            with smtplib.SMTP(self.email_host, self.email_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
                logging.info("E-mail enviado com sucesso.")
        except smtplib.SMTPAuthenticationError as e:
            logging.error(f"Erro de autenticação SMTP: {e}")
            raise e
        except Exception as e:
            logging.error(f"Erro ao enviar e-mail: {e}")
            raise e

class EmailContentFormatter:
    @staticmethod
    def format_weekly_digest(top_recipes):
        recipe_list = "".join(
            [
                (
                    f"<div style='margin-bottom: 24px; border: 1px solid #e0e0e0; padding: 20px; border-radius: 8px; background-color: #fff8f4;'>\n"
                    f"  <h3 style='color: #bf360c; margin: 0; font-size: 20px;'>{r['nomeReceita']}</h3>\n"
                    f"  <p style='margin: 10px 0; font-size: 15px; color: #5d4037;'>{r.get('descricaoReceita', 'Essa receita ainda não tem descrição, mas com certeza guarda memórias deliciosas!')}</p>\n"
                    f"  <div style='margin-top: 10px;'>\n"
                    + "".join(
                        [
                            f"<span style='display: inline-block; background-color: #ffe0b2; color: #6d4c41; font-size: 13px; padding: 4px 10px; border-radius: 15px; margin-right: 6px; margin-bottom: 6px;'>💛 {emo}</span>"
                            for emo in r.get('sentimentoReceita', [])
                        ]
                    )
                    + "\n  </div>\n"
                    f"</div>\n"
                )
                for r in top_recipes
            ]
        )

        return (
            f"<html>\n"
            f"<body style='font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 30px;'>\n"
            f"  <div style='max-width: 600px; margin: auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);'>\n"
            f"    <h1 style='color: #bf360c; text-align: center; font-size: 26px;'>✨ Receitas mais queridas da semana ✨</h1>\n"
            f"    <p style='text-align: center; font-size: 16px; color: #6d4c41;'>Olá! Estas são as receitas que mais despertaram emoções nesta semana no <strong>Memórias à Mesa</strong>:</p>\n"
            f"    {recipe_list}\n"
            f"    <div style='text-align: center; margin-top: 30px;'>\n"
            f"      <a href='https://memoriasamesa-728b.vercel.app/listareceitas' "
            f"        style='display: inline-block; padding: 12px 24px; background-color: #ff5722; color: white; "
            f"        text-decoration: none; border-radius: 6px; font-size: 15px;'>🍲 Ver Receitas</a>\n"
            f"    </div>\n"
            f"    <p style='text-align: center; margin-top: 30px; font-size: 14px; color: #999;'>Com carinho,<br>Equipe Memórias à Mesa 💛</p>\n"
            f"  </div>\n"
            f"</body>\n"
            f"</html>"
        )

class SchedulerService:
    def _init_(self, scheduler: AsyncIOScheduler, email_service: EmailService, user_service: UserService, receita_service: ReceitaService):
        # Armazenamento dos serviços como atributos da classe
        self.scheduler = scheduler
        self.email_service = email_service
        self.user_service = user_service
        self.receita_service = receita_service

    def start_scheduler(self):
        # REMOVIDO: a função sync_send_weekly_emails e o gerenciamento manual do loop
        #           O AsyncIOScheduler gerencia isso por você.

        logging.info("Iniciando o método start_scheduler...")
        logging.info("Configurando o job para envio semanal de emails...")

        if self.scheduler.running:
            logging.info("Scheduler já está em execução.")
        else:
            logging.info("Iniciando o scheduler pela primeira vez.")

        # MUDANÇA CRUCIAL AQUI: Adicionando a função async diretamente ao scheduler
        self.scheduler.add_job(self.send_weekly_emails, 'cron', day_of_week='wed', hour=20, minute=15)
        logging.info("Job de envio semanal configurado com sucesso.")

        # O scheduler será iniciado pela função lifespan do FastAPI, não aqui.
        # self.scheduler.start() # Removido para evitar múltiplas chamadas de start
        logging.info("Scheduler configurado. Aguardando o início do FastAPI.")

    async def send_weekly_emails(self):
        logging.info("Executando send_weekly_emails (assíncrono)...")
        try:
            top_recipes = await self.receita_service.get_fav_recipes_for_the_week()
            users = await self.user_service.get_all_users_emails()

            email_body = EmailContentFormatter.format_weekly_digest(top_recipes)

            for user_email in users: # Renomeado 'user' para 'user_email' para clareza
                # A função send_email é síncrona, então não precisa de await
                self.email_service.send_email(user_email, "💌 Memórias que aquecem: veja as receitas mais amadas da semana", email_body)
            logging.info("Todos os e-mails semanais foram processados.")
        except Exception as e:
            logging.error(f"Erro na execução de send_weekly_emails: {e}")
            # Você pode querer relançar a exceção ou lidar com ela de forma mais granular
            # raise e

_all_ = ["start_scheduler", "send_weekly_emails"] # 'start_scheduler' não é importado diretamente, mas é um bom hábito.