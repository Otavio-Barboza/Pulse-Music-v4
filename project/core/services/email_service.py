import smtplib, dotenv, os
from email.message import EmailMessage
from datetime import datetime

dotenv.load_dotenv(r'Assets\App\Env\.env')
SENHA_APP = os.getenv('SENHA_APP')

def enviar_email_suporte(
    mensagem: str,
    email_usuario: str,
    assunto: str = "Pulse Music | Nova mensagem de suporte"
):
    EMAIL_SUPORTE = "barbozaotavio17@gmail.com"
    EMAIL_APP = "otolif2023@gmail.com"
    EMAIL_USER = email_usuario

    data_hora = datetime.now().strftime("%d/%m/%Y às %H:%M")

    msg = EmailMessage()
    msg["From"] = EMAIL_APP
    msg["To"] = EMAIL_SUPORTE
    msg['Reply-To'] = EMAIL_USER
    msg["Subject"] = assunto

    msg.set_content(f"""
📬 Nova mensagem recebida pelo Pulse Music

👤 Usuário: {email_usuario}
🕒 Data/Hora: {data_hora}

📝 Mensagem:\n
{mensagem}
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_APP, SENHA_APP)
        smtp.send_message(msg)