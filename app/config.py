from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class Config:
    secret_key = os.environ.get("SECRET_KEY")
    admin_key = os.environ.get("ADMIN_KEY")
    server_host = os.environ.get("SERVER_HOST")
    db_host = os.environ.get("DB_HOST")
    db_username = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    db_port = int(os.environ.get("DB_PORT"))
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS\
        = bool(os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS"))
    SQLALCHEMY_ECHO = bool(os.environ.get("SQLALCHEMY_ECHO"))
    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
