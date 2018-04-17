from flask import Blueprint
from flask_restful import (Resource, reqparse, marshal_with,
                           Api)

from app.database.models import User
from app.managers.signin import SigninManager
from app.utils.errors import UserDoesntExistsError, \
                             UserPasswordIncorrectError, \
                             EmailNotVerifiedError
from app.v1.controllers.users import user_fields

signin_reqparser = reqparse.RequestParser()
signin_reqparser.add_argument('email', type=str, trim=True,
                              location=['form', 'json'],
                              required=True, nullable=False,
                              help='No user email provided')
signin_reqparser.add_argument('password', type=str, trim=False,
                              location=['form', 'json'],
                              required=True, nullable=False,
                              help='No user email provided')


def get_is_identified(user, password):
    return user.password == password


class SigninResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        user = User.query.filter_by(_id=SigninManager.get_user_id()).first()

        return user

    @marshal_with(user_fields)
    def post(self):
        args = signin_reqparser.parse_args()
        user = User.query.filter_by(email=args["email"]).first()
        if user is None:
            raise UserDoesntExistsError(
                "User {} doesn\'t exists.".format(args["email"]))

        if not get_is_identified(user, args["password"]):
            raise UserPasswordIncorrectError(
                "User password is incorrect.")

        # E-mail verification check
        if user.verifyemails.first().is_verified is False:
            raise EmailNotVerifiedError("User email was not verified.")

        SigninManager.set_is_signed_in(True)
        SigninManager.set_user_id(user._id)

        return user


signin_api = Blueprint('resources.signin', __name__)
api = Api(signin_api)
api.add_resource(
    SigninResource,
    '',
    endpoint='signin'
)
