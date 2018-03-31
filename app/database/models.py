from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from app.database import Base


class Library(Base):
    __tablename__ = 'Libraries'

    _id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    location_road = Column('location_road', String)
    location_number = Column('location_number', String)
    location_detail = Column('location_detail', String)
    manager_name = Column('manager_name', String)
    manager_email = Column('manager_email', String)
    manager_phone = Column('manager_phone', String)
    audiences = Column('audiences', String)
    fac_beam_screen = Column('fac_beam_screen', TINYINT)
    fac_sound = Column('fac_sound', TINYINT)
    fac_record = Column('fac_record', TINYINT)
    fac_placard = Column('fac_placard', TINYINT)
    fac_self_promo = Column('fac_self_promo', TINYINT)
    fac_other = Column('fac_other', String)
    req_speaker = Column('req_speaker', String)
