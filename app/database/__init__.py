from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import Config

engine = create_engine(Config.db_uri, echo=True, convert_unicode=True)
db = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db.query_property()


def initialize_database():
    Base.metadata.create_all(bind=engine)
