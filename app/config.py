from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

class Config:
    secret_key = os.environ.get("SECRET_KEY")
    db_host = os.environ.get("DB_HOST")
    db_username = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    db_port = int(os.environ.get("DB_PORT"))
    db_uri = os.environ.get("SQLALCHEMY_DATABASE_URI")
