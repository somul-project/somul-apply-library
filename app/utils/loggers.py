import json

from pymysql import IntegrityError

from app import db
from app.database.logger_models import LOGTYPE, Log


def log_request(content):
    return _log_on_db(LOGTYPE.REQUEST, content)


def log_response(content):
    return _log_on_db(LOGTYPE.RESPONSE, content)


def _log_on_stdout(content):
    print(content)


def _log_on_db(logtype, content):
    instance = Log(logtype=logtype, content=json.dumps(content))
    try:
        db.session.add(instance)
        db.session.commit()
    except IntegrityError as e:
        print(str(e))
        db.session.rollback()
        return False
    except Exception as e:
        print(str(e))
        db.session.rollback()
        return False

    return True
