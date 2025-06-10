import os
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
import asyncio
import smtplib
from email.message import EmailMessage
from service.service_receita import get_fav_recipes_for_the_week as get_top_recipes
from service.service_user import UserService
from repositories.repository_user import UserRepositoryMongo
from service.service_user import UserValidationService
import logging

email_user = os.getenv("EMAIL")
email_password = os.getenv("SENHAEMAIL")

brasil_timezone = timezone("America/Sao_Paulo")
scheduler = BackgroundScheduler(timezone=brasil_timezone)

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Instanciar dependências
repository = UserRepositoryMongo() 
validation_service = UserValidationService()
user_service = UserService(repository=repository, validation_service=validation_service)

def start_scheduler():
    # Wrapper síncrono para chamar a função assíncrona
    def sync_send_weekly_emails():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(send_weekly_emails())
        finally:
            loop.close()  

    logging.info("Iniciando o scheduler...")

    # Executa toda quarta-feira às 21h no horário de Brasília
    scheduler.add_job(sync_send_weekly_emails, 'cron', day_of_week='wed', hour=21, minute=8)
    logging.info("Job de envio semanal configurado para quarta-feira às 21:08 no horário de Brasília.")

    scheduler.start()
    logging.info("Scheduler iniciado.")

def send_email(to_address: str, subject: str, body: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = to_address
    msg.add_alternative(body, subtype='html')
    email_host = "smtp.gmail.com"
    email_port = 587

    logging.info(f"Enviando e-mail para {to_address} com assunto '{subject}'...")

    try:
        with smtplib.SMTP(email_host, int(email_port)) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)
            logging.info("E-mail enviado com sucesso.")
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"Erro de autenticação SMTP: {e}")
        raise e
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail: {e}")
        raise e

async def send_weekly_emails():
    top_recipes = await get_top_recipes()
    users = await user_service.get_all_users_emails()

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

    email_body = (
        f"<html>\n"
        f"<body style='font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 30px;'>\n"
        f"  <div style='max-width: 600px; margin: auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);'>\n"
        f"    <h1 style='color: #bf360c; text-align: center; font-size: 26px;'>✨ Receitas mais queridas da semana ✨</h1>\n"
        f"    <p style='text-align: center; font-size: 16px; color: #6d4c41;'>Olá! Estas são as receitas que mais despertaram emoções nesta semana no <strong>Memórias à Mesa</strong>:</p>\n"
        f"    {recipe_list}\n"
        f"    <div style='text-align: center; margin-top: 30px;'>\n"
        f"      <a href='https://memoriasamesa-728b.vercel.app/listareceitas' "
        f"         style='display: inline-block; padding: 12px 24px; background-color: #ff5722; color: white; "
        f"         text-decoration: none; border-radius: 6px; font-size: 15px;'>🍲 Ver Receitas</a>\n"
        f"    </div>\n"
        f"    <p style='text-align: center; margin-top: 30px; font-size: 14px; color: #999;'>Com carinho,<br>Equipe Memórias à Mesa 💛</p>\n"
        f"  </div>\n"
        f"</body>\n"
        f"</html>"
    )

    for user in users:
        send_email(user, "💌 Memórias que aquecem: veja as receitas mais amadas da semana", email_body)