from hashlib import sha256

from flask_restful import reqparse

from app.config import Config
from app.utils.errors import WrongSecretkeyError


HEADER_SECRET_KEYS = ["Secret-Key", "Secret_Key"]
secretkey_reqparser = reqparse.RequestParser()
secretkey_reqparser.add_argument(HEADER_SECRET_KEYS[0], type=str,
                                 location=['headers', 'args'])
secretkey_reqparser.add_argument(HEADER_SECRET_KEYS[1], type=str,
                                 location=['headers', 'args'])


class CredentialManager:
    @classmethod
    def digest_from_plainstr(cls, key):
        encoded = key.encode('utf-8')

        return sha256(encoded).digest()

    @classmethod
    def get_secret_key(cls):
        args = secretkey_reqparser.parse_args()
        if args[HEADER_SECRET_KEYS[0]] is not None:
            return args[HEADER_SECRET_KEYS[0]]
        else:
            return args[HEADER_SECRET_KEYS[1]]

    @classmethod
    def get_is_admin(cls):
        secret_key = cls.get_secret_key()

        disgested = cls.digest_from_plainstr(secret_key)
        stored_digested = cls.digest_from_plainstr(Config.admin_key)

        if disgested == stored_digested:
            return True
        else:
            raise WrongSecretkeyError(
                "{} is incorrect.".format(secret_key))
