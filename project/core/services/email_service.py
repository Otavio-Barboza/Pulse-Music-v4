# imports gerais
from email.message import EmailMessage
from datetime import datetime
import smtplib, dotenv, os


dotenv.load_dotenv(r'Assets\App\Env\.env')
SENHA_APP = os.getenv('SENHA_APP')


def send_email(
    message: str,
    email_user: str,
    subject: str = "Pulse Music | Nova mensagem de suporte"
):
    EMAIL_SUPORTE = "barbozaotavio17@gmail.com"
    EMAIL_APP = "otolif2023@gmail.com"
    EMAIL_USER = email_user

    date_hours = datetime.now().strftime("%d/%m/%Y às %H:%M")

    msg = EmailMessage()
    msg["From"] = EMAIL_APP
    msg["To"] = EMAIL_SUPORTE
    msg['Reply-To'] = EMAIL_USER
    msg["Subject"] = subject

    msg.set_content(
        f"""
        📬 Nova mensagem recebida pelo Pulse Music

        👤 Usuário: {email_user}
        🕒 Data/Hora: {date_hours}

        📝 Mensagem:\n
        {message}
        """
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_APP, SENHA_APP)
        smtp.send_message(msg)