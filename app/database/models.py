from datetime import datetime

from pytz import timezone
from sqlalchemy import Text
from sqlalchemy.dialects.mysql import TINYINT, INTEGER
from sqlalchemy.orm import validates

from app.utils.errors import InvalidArgumentError
from app.database import db
from app.utils.validators import is_valid_email, has_valid_length, \
    is_valid_phone

PASSWORD_LENGTH_MINIMUM = 8
PASSWORD_LENGTH_MAXIMUM = 20
TIMEZONE_ASIA_SEOUL = "Asia/Seoul"


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


session_time_choices = ["14:00", "15:00"]


def now_at_seoul():
    return datetime.now(tz=timezone(TIMEZONE_ASIA_SEOUL))


def elapsed_datetime_at_seoul(seoultime):
    if seoultime.tzinfo is None:
        seoultime = seoultime.replace(tzinfo=timezone(TIMEZONE_ASIA_SEOUL))

    return seoultime - now_at_seoul()


class TimestampMixin(object):
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=now_at_seoul)
    updated_at = db.Column(db.DateTime,
                           nullable=True,
                           onupdate=now_at_seoul)


class User(db.Model, TimestampMixin):
    _id = db.Column('id', db.Integer, primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    phone = db.Column(db.String(30), nullable=False)

    password = db.Column(db.String(30), nullable=False)
    has_experienced_somul = db.Column(db.Boolean, nullable=False,
                                      default=False)
    library_id = db.Column(INTEGER(11, unsigned=True),
                           db.ForeignKey('Libraries.id'),
                           nullable=True)
    library = db.relationship('Library', lazy=True,
                              backref=db.backref('users', lazy=True))

    verifyemails = db.relationship('VerifyEmail',
                                   backref=db.backref('user', uselist=False),
                                   lazy='dynamic',
                                   cascade="delete")

    @validates('name')
    def validate_not_empty(self, key, field):
        if not field:
            raise InvalidArgumentError("{} must be not empty.".format(key))

        return field

    @validates('email')
    def validate_email_format(self, key, field):
        if not is_valid_email(field):
            raise InvalidArgumentError(
                "{} must be fitted in email format.".format(key))

        return field

    @validates('password')
    def validate_password_length(self, key, field):
        if not has_valid_length(field,
                                PASSWORD_LENGTH_MINIMUM,
                                PASSWORD_LENGTH_MAXIMUM):
            raise InvalidArgumentError(
                "{}'s length must be {} ~ {}.".format(
                    key, PASSWORD_LENGTH_MINIMUM, PASSWORD_LENGTH_MAXIMUM))

        return field

    @validates('phone')
    def validate_phone_format(self, key, field):
        if not is_valid_phone(field):
            raise InvalidArgumentError(
                "{} must be fitted in phone number format.".format(key))

        return field

    def __repr__(self):
        return '<%r %r>' % (self.__class__.__name__, self.name)


class SpeakerInfo(db.Model, TimestampMixin):
    _id = db.Column('id', db.Integer, primary_key=True,
                    autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    user = db.relationship('User', lazy=True,
                           backref=db.backref('speakerinfo',
                                              lazy=True, uselist=False))

    session_time = db.Column(db.String(15), nullable=False, default="")
    introduce = db.Column(db.Text, nullable=False, default="")
    history = db.Column(db.Text, nullable=False, default="")
    keynote_link = db.Column(db.Text, nullable=True)
    admin_approved = db.Column(db.Boolean, nullable=True)

    title = db.Column(db.String(256), nullable=False, default="")
    description = db.Column(db.Text, nullable=False, default="")

    @validates('session_time')
    def validate_session_time(self, key, field):
        if field not in session_time_choices:
            raise InvalidArgumentError("{} must be in {}."
                                       .format(key, session_time_choices))

        return field

    def __repr__(self):
        return '<%r %r>' % (self.__class__.__name__, self.name)


class VerifyEmail(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True,
                    autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)

    key = db.Column(db.String(40), unique=True, nullable=False, default="")
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    sended_at = db.Column(db.DateTime, nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)
    expired = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<%r %r>' % (self.__class__.__name__, self.name)
