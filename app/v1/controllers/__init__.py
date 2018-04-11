from hashlib import sha256

from flask_restful import reqparse

from app.config import Config
from app.database import db
from app.utils.errors import DataNotFoundError, WrongSecretkeyError


def get_or_404(model_clazz, pk):
    instance = model_clazz.query.filter_by(_id=pk).first()
    if instance is None:
        raise DataNotFoundError(
            "{} {} Not found".format(model_clazz.__name__, pk))

    return instance


secretkey_reqparser = reqparse.RequestParser()
secretkey_reqparser.add_argument('secretkey', type=str,
                                 location='headers')


def digest_from_plainstr(key):
    encoded = key.encode('utf-8')

    return sha256(encoded).digest()


def get_is_admin():
    args = secretkey_reqparser.parse_args()
    if args.secretkey is None:
        return False

    disgested = digest_from_plainstr(args.secretkey)
    stored_digested = digest_from_plainstr(Config.secret_key)

    if disgested == stored_digested:
        return True
    else:
        raise WrongSecretkeyError("Secretkey is incorrect.")
