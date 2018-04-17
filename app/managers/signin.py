from flask import session

from app.utils.errors import UserSessionEmptyError

SESSIONKEY_IS_SIGNED_IN = "is_signed_in"
SESSIONKEY_USER_ID = "user_id"


class SigninManager:
    @classmethod
    def get_is_signed_in(cls):
        if SESSIONKEY_IS_SIGNED_IN not in session:
            return False

        return session[SESSIONKEY_IS_SIGNED_IN]

    @classmethod
    def set_is_signed_in(cls, is_signed_in):
        session[SESSIONKEY_IS_SIGNED_IN] = is_signed_in

    @classmethod
    def get_user_id(cls):
        if SESSIONKEY_USER_ID not in session:
            raise UserSessionEmptyError("User session empty error.")

        return session[SESSIONKEY_USER_ID]

    @classmethod
    def set_user_id(cls, user_id):
        session[SESSIONKEY_USER_ID] = user_id
