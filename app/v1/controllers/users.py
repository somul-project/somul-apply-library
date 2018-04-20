from flask import Blueprint
from flask_restful import (Resource, reqparse, fields,
                           marshal_with, Api)
from sqlalchemy.exc import IntegrityError

from app.database import db, get_or_404, now_at_seoul
from app.database.models import User, VerifyEmail
from app.utils.errors import abort_with_integrityerror, UnauthorizedError, \
    EmailNotSendedError
from app.managers.credential import CredentialManager
from app.managers.email import EmailManager


user_fields = {
    '_id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,

    'has_experienced_somul': fields.Boolean,
    'library_id': fields.Integer,

    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
}

user_reqparser = reqparse.RequestParser()
user_reqparser.add_argument('name', type=str, trim=True,
                            location=['form', 'json'],
                            required=True, nullable=False,
                            help='No user name provided')
user_reqparser.add_argument('email', type=str, trim=True,
                            location=['form', 'json'],
                            required=True, nullable=False,
                            help='No user email provided')
user_reqparser.add_argument('phone', type=str, trim=True,
                            location=['form', 'json'],
                            required=True, nullable=False,
                            help='No user phone provided')

user_reqparser.add_argument('password', type=str, trim=False,
                            location=['form', 'json'],
                            required=True, nullable=False,
                            help='No user password provided')
user_reqparser.add_argument('has_experienced_somul', type=bool,
                            location=['form', 'json'],
                            required=False, nullable=False,
                            help='No user has_experienced_somul provided')


class UserListResource(Resource):
    def __init__(self):
        super().__init__()

    @marshal_with(user_fields)
    def get(self):
        if not CredentialManager.get_is_admin():
            raise UnauthorizedError("Unauthorized.")

        users = User.query.all()

        return users

    @marshal_with(user_fields)
    def post(self):
        args = user_reqparser.parse_args()

        user = User(**args)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            abort_with_integrityerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        # E-mail Integration
        gen_uuid = EmailManager.get_unique_uuid()
        email = VerifyEmail(
            user_id=user._id,
            key=gen_uuid
        )

        if EmailManager.send_verify_email(user.email, gen_uuid):
            email.sended_at = now_at_seoul()
        else:
            raise EmailNotSendedError()

        try:
            db.session.add(email)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            abort_with_integrityerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return user


class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, pk):
        if not CredentialManager.get_is_admin():
            raise UnauthorizedError("Unauthorized.")

        user = get_or_404(User, pk)

        return user

    @marshal_with(user_fields)
    def put(self, pk):
        args = user_reqparser.parse_args()
        user = get_or_404(User, pk)

        for key, value in args.items():
            if value is None:
                continue

            setattr(user, key, value)

        try:
            db.session.merge(user)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            abort_with_integrityerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return user

    def delete(self, pk):
        if not CredentialManager.get_is_admin():
            raise UnauthorizedError("Unauthorized.")

        user = get_or_404(User, pk)

        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return '', 204


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserListResource,
    '',
    endpoint='users'
)

api.add_resource(
    UserResource,
    '/<int:pk>',
    endpoint='user'
)
