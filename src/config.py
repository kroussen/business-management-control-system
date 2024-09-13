import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('../.env'))

BASE_DIR = Path(__file__).parent


class AuthJWT:
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 1440


class Settings:
    MODE: str = os.environ.get('MODE')

    DB_HOST: str = os.environ.get('DB_HOST')
    DB_PORT: int = os.environ.get('DB_PORT')
    DB_USER: str = os.environ.get('DB_USER')
    DB_PASS: str = os.environ.get('DB_PASS')
    DB_NAME: str = os.environ.get('DB_NAME')

    DB_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    auth_jwt = AuthJWT()

    MAIL_USERNAME: str = os.environ.get('MAIL_USERNAME')
    MAIL_FROM: str = os.environ.get('MAIL_FROM')
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER: str = os.environ.get('MAIL_SERVER')
    MAIL_PORT: str = os.environ.get('MAIL_PORT')


settings = Settings()
