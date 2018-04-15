from hashlib import sha256

from flask_restful import reqparse

from app.config import Config
from app.utils.errors import WrongSecretkeyError


HEADER_SECRET_KEY = "Secret-Key"
secretkey_reqparser = reqparse.RequestParser()
secretkey_reqparser.add_argument(HEADER_SECRET_KEY, type=str,
                                 location='headers')


class CredentialManager:
    @classmethod
    def digest_from_plainstr(cls, key):
        encoded = key.encode('utf-8')

        return sha256(encoded).digest()

    @classmethod
    def get_is_admin(cls):
        args = secretkey_reqparser.parse_args()
        if args[HEADER_SECRET_KEY] is None:
            return False

        disgested = cls.digest_from_plainstr(args[HEADER_SECRET_KEY])
        stored_digested = cls.digest_from_plainstr(Config.secret_key)

        if disgested == stored_digested:
            return True
        else:
            raise WrongSecretkeyError(
                "{} is incorrect.".format(HEADER_SECRET_KEY))
