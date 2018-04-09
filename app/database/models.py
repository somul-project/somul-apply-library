from sqlalchemy import Column, Text
from sqlalchemy.dialects.mysql import TINYINT, INTEGER
from sqlalchemy.orm import validates

from app.database import Base
from app.utils.errors import InvalidArgumentError


class Library(Base):
    __tablename__ = 'Libraries'

    _id = Column('id',
                 INTEGER(11, unsigned=True),
                 primary_key=True,
                 autoincrement=True)
    name = Column('name', Text)
    location_road = Column('location_road', Text)
    location_number = Column('location_number', Text)
    location_detail = Column('location_detail', Text)

    manager_name = Column('manager_name', Text)
    manager_email = Column('manager_email', Text)
    manager_phone = Column('manager_phone', Text)
    audiences = Column('audiences', Text)

    fac_beam_screen = Column('fac_beam_screen', TINYINT(1))
    fac_sound = Column('fac_sound', TINYINT(1))
    fac_record = Column('fac_record', TINYINT(1))
    fac_placard = Column('fac_placard', TINYINT(1))
    fac_self_promo = Column('fac_self_promo', TINYINT(1))

    fac_other = Column('fac_other', Text)
    req_speaker = Column('req_speaker', Text)

    @validates('name')
    def validate_not_empty(self, key, field):
        if not field:
            raise InvalidArgumentError("{} must be not empty.".format(key))

        return field
