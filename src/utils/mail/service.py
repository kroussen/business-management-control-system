from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

from config import settings


class EmailService:
    def __init__(self):
        self.email_config = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        self.fast_api_mail = FastMail(self.email_config)

    async def send_email(self, subject: str, email: EmailStr, html_content: str):
        message = MessageSchema(subject=subject, recipients=[email], body=html_content, subtype="html", )
        await self.fast_api_mail.send_message(message)

    async def send_invite_email(self, email: EmailStr, token: str):
        html = f"""Код для подтверждения E-mail: {token}"""
        await self.send_email("Код подтверждения", email, html)

    async def send_invite_employee(self, email: EmailStr, invite_url: str):
        html = f"""
                <br>Email: {email}
                <br>Url: {invite_url}
                """
        await self.send_email("Пригласительная ссылка", email, html)
