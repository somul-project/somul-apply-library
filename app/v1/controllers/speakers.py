from flask import Blueprint
from flask_restful import (Resource, reqparse, fields,
                           marshal_with, Api, marshal)
from sqlalchemy.exc import IntegrityError

from app.database import db
from app.database.models import Speaker, session_time_choices
from app.utils.errors import DuplicatedDataError
from app.v1.controllers import get_or_404, get_is_admin


speaker_fields = {
    '_id': fields.Integer,
    'name': fields.String,

    'is_email_verified': fields.Boolean,
    'email_sended_at': fields.DateTime,

    'session_time': fields.String,

    'library_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
}


speaker_fields_including_protected = {
    **speaker_fields,
    'email': fields.String,
    'phone': fields.String,
}


speaker_reqparser = reqparse.RequestParser()
speaker_reqparser.add_argument('name', type=str, trim=True,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No speaker name provided')
speaker_reqparser.add_argument('email', type=str, trim=True,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No speaker email provided')
speaker_reqparser.add_argument('phone', type=str, trim=True,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No speaker phone provided')

speaker_reqparser.add_argument('password', type=str,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No speaker phone provided')
speaker_reqparser.add_argument('session_time',
                               choices=session_time_choices,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No speaker session_time provided')
speaker_reqparser.add_argument('library_id', type=int,
                               location=['form', 'json'],
                               required=True, nullable=False,
                               help='No speaker library_id provided')


def get_is_identified():
    return True


class SpeakerListResource(Resource):
    def __init__(self):
        super().__init__()

    def get(self):
        speakers = Speaker.query.all()

        resp_fields = speaker_fields
        if get_is_admin() or get_is_identified():
            resp_fields = speaker_fields_including_protected

        return marshal(speakers, resp_fields)

    def post(self):
        args = speaker_reqparser.parse_args()

        speaker = Speaker(**args)

        try:
            db.session.add(speaker)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            raise DuplicatedDataError(str(e.orig))
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return marshal(speaker, speaker_fields_including_protected)


class SpeakerResource(Resource):
    def get(self, pk):
        speaker = get_or_404(Speaker, pk)

        resp_fields = speaker_fields
        if get_is_admin():
            resp_fields = speaker_fields_including_protected

        return marshal(speaker, resp_fields)

    @marshal_with(speaker_fields)
    def put(self, pk):
        args = speaker_reqparser.parse_args()
        speaker = get_or_404(Speaker, pk)

        for key, value in args.items():
            if value is None:
                continue

            setattr(speaker, key, value)

        try:
            db.session.merge(speaker)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            raise DuplicatedDataError(str(e.orig))
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return speaker

    def delete(self, pk):
        speaker = get_or_404(Speaker, pk)

        try:
            db.session.delete(speaker)
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return '', 204


speakers_api = Blueprint('resources.speakers', __name__)
api = Api(speakers_api)
api.add_resource(
    SpeakerListResource,
    '/speaker',
    endpoint='speakers'
)

api.add_resource(
    SpeakerResource,
    '/speaker/<int:pk>',
    endpoint='speaker'
)
