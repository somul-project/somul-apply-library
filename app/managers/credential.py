from hashlib import sha256

from flask_restful import reqparse

from app.config import Config
from app.utils.errors import WrongSecretkeyError


secretkey_reqparser = reqparse.RequestParser()
secretkey_reqparser.add_argument('Secret-Key', type=str,
                                 location='headers')


class CredentialManager:
    @classmethod
    def digest_from_plainstr(cls, key):
        encoded = key.encode('utf-8')

        return sha256(encoded).digest()

    @classmethod
    def get_is_admin(cls):
        args = secretkey_reqparser.parse_args()
        if args.secretkey is None:
            return False

        disgested = cls.digest_from_plainstr(args.secretkey)
        stored_digested = cls.digest_from_plainstr(Config.secret_key)

        if disgested == stored_digested:
            return True
        else:
            raise WrongSecretkeyError("Secretkey is incorrect.")
