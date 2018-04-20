from datetime import datetime
from pytz import timezone

from flask_sqlalchemy import SQLAlchemy

from app.utils.errors import DataNotFoundError


db = SQLAlchemy()
TIMEZONE_ASIA_SEOUL = "Asia/Seoul"


def get_or_404(model_clazz, pk):
    instance = get_or_none(model_clazz, pk)
    if instance is None:
        raise DataNotFoundError(
            "{} {} Not found".format(model_clazz.__name__, pk))

    return instance


def get_or_none(model_clazz, pk):
    return model_clazz.query.filter_by(_id=pk).first()


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
