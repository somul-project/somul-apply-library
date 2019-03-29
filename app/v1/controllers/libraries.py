from flask import Blueprint
from flask_restful import (Resource, reqparse, fields,
                           marshal_with, Api, marshal)
from sqlalchemy.exc import IntegrityError

from app.database import db, get_or_404
from app.database.models import Library
from app.managers.credential import CredentialManager
from app.utils.errors import abort_with_integrityerror


library_fields = {
    '_id': fields.Integer,
    'name': fields.String,
    'location_road': fields.String,
    'location_number': fields.String,
    'location_detail': fields.String,

    'audiences': fields.String,

    'fac_beam_screen': fields.Boolean,
    'fac_sound': fields.Boolean,
    'fac_record': fields.Boolean,
    'fac_placard': fields.Boolean,
    'fac_self_promo': fields.Boolean,

    'fac_other': fields.String,
    'req_speaker': fields.String,
}

library_protected_fields = {
    'manager_name': fields.String,
    'manager_email': fields.String,
    'manager_phone': fields.String,
}


library_reqparser = reqparse.RequestParser()
library_reqparser.add_argument('name', type=str, trim=True,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library name provided')
library_reqparser.add_argument('location_road', type=str, trim=True,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library location_road provided')
library_reqparser.add_argument('location_number', type=str, trim=True,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library location_number provided')
library_reqparser.add_argument('location_detail', type=str, trim=True,
                               location=['form', 'json'],
                               required=False)

library_reqparser.add_argument('manager_name', type=str, trim=True,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library manager_name provided')
library_reqparser.add_argument('manager_email', type=str, trim=True,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library manager_email provided')
library_reqparser.add_argument('manager_phone', type=str, trim=True,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library manager_phone provided')
library_reqparser.add_argument('audiences', type=str, trim=True,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library audiences provided')

library_reqparser.add_argument('fac_beam_screen', type=bool,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library fac_beam_screen provided')
library_reqparser.add_argument('fac_sound', type=bool,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library fac_sound provided')
library_reqparser.add_argument('fac_record', type=bool,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library fac_record provided')
library_reqparser.add_argument('fac_placard', type=bool,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library fac_placard provided')
library_reqparser.add_argument('fac_self_promo', type=bool,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No library fac_self_promo provided')

library_reqparser.add_argument('fac_other', type=str, trim=True,
                               location=['form', 'json'],
                               required=False)
library_reqparser.add_argument('req_speaker', type=str, trim=True,
                               location=['form', 'json'],
                               required=False)


class LibraryListResource(Resource):
    def get(self):
        libraries = Library.query.all()

        resp_fields = library_fields
        if CredentialManager.get_is_admin():
            resp_fields = {**library_fields, **library_protected_fields}

        return marshal(libraries, resp_fields)

    @marshal_with(library_fields)
    def post(self):
        args = library_reqparser.parse_args()

        library = Library(**args)

        try:
            db.session.add(library)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            abort_with_integrityerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return library


class LibraryResource(Resource):
    def get(self, pk):
        library = get_or_404(Library, pk)

        resp_fields = library_fields
        if CredentialManager.get_is_admin():
            resp_fields = {**library_fields, **library_protected_fields}

        return marshal(library, resp_fields)

    @marshal_with(library_fields)
    def put(self, pk):
        args = library_reqparser.parse_args()
        library = get_or_404(Library, pk)

        for key, value in args.items():
            if value is None:
                continue

            setattr(library, key, value)

        try:
            db.session.merge(library)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            abort_with_integrityerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return library

    def delete(self, pk):
        library = get_or_404(Library, pk)

        try:
            db.session.delete(library)
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return '', 204


class LibraryDetailResource(Resource):
    def get(self, phone_number):
        library = Library.query.filter_by(manager_phone=phone_number).first()
        print(library)
        return "test", 200


libraries_api = Blueprint('resources.libraries', __name__)
api = Api(libraries_api)
api.add_resource(
    LibraryListResource,
    '',
    endpoint='libraries'
)

api.add_resource(
    LibraryResource,
    '/<int:pk>',
    endpoint='library'
)

api.add_resource(
    LibraryDetailResource,
    '/detail/<string:phone_number>',
    endpoint='detail'
)
