from sqlalchemy import Text
from sqlalchemy.dialects.mysql import TINYINT, INTEGER
from sqlalchemy.orm import validates

from app.utils.errors import InvalidArgumentError
from app.database import db


class Library(db.Model):
    __tablename__ = 'Libraries'

    _id = db.Column('id',
                    INTEGER(11, unsigned=True),
                    primary_key=True,
                    autoincrement=True)
    name = db.Column('name', Text)
    location_road = db.Column('location_road', Text)
    location_number = db.Column('location_number', Text)
    location_detail = db.Column('location_detail', Text)

    manager_name = db.Column('manager_name', Text)
    manager_email = db.Column('manager_email', Text)
    manager_phone = db.Column('manager_phone', Text)
    audiences = db.Column('audiences', Text)

    fac_beam_screen = db.Column('fac_beam_screen', TINYINT(1))
    fac_sound = db.Column('fac_sound', TINYINT(1))
    fac_record = db.Column('fac_record', TINYINT(1))
    fac_placard = db.Column('fac_placard', TINYINT(1))
    fac_self_promo = db.Column('fac_self_promo', TINYINT(1))

    fac_other = db.Column('fac_other', Text)
    req_speaker = db.Column('req_speaker', Text)

    @validates('name')
    def validate_not_empty(self, key, field):
        if not field:
            raise InvalidArgumentError("{} must be not empty.".format(key))

        return field

    def __repr__(self):
        return '<Library %r>' % self.name
