from flask import Blueprint
from flask_restful import (Resource, reqparse, marshal_with,
                           Api)

from app.database.models import User
from app.utils.errors import UserDoesntExistsError, UserPasswordIncorrectError
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
    return user["password"] == password


class SigninResource(Resource):
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

        return user


signin_api = Blueprint('resources.signin', __name__)
api = Api(signin_api)
api.add_resource(
    SigninResource,
    '/signin',
    endpoint='signin'
)
