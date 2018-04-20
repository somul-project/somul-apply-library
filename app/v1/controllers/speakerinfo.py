from flask import Blueprint, request
from flask_restful import (Resource, reqparse, fields,
                           marshal_with, Api)

from app.database import get_or_404, db
from app.database.models import SpeakerInfo
from app.database.speakerinfo import SpeakerInfoRepo
from app.managers.credential import CredentialManager
from app.managers.signin import SigninManager
from sqlalchemy.exc import IntegrityError
from app.utils.errors import UnauthorizedError, \
                             SigninRequiredError, \
                             abort_with_integrityerror

import json

speakerinfo_fields = {
    '_id': fields.Integer,
    'user_id': fields.Integer,

    'session_time': fields.String,
    'introduce': fields.String,
    'history': fields.String,
    'keynote_link': fields.String,
    'admin_approved': fields.Boolean,

    'title': fields.String,
    'description': fields.String,
}


speakerinfo_reqparser = reqparse.RequestParser()
speakerinfo_reqparser.add_argument('session_time', type=str, trim=True,
                                   location=['form', 'json'],
                                   required=False, nullable=True,
                                   help='No speakerinfo session_time provided')
speakerinfo_reqparser \
    .add_argument('introduce', type=str, trim=True,
                  location=['form', 'json'],
                  required=False, nullable=False,
                  help='No speakerinfo introduce provided')
speakerinfo_reqparser.add_argument('history', type=str, trim=True,
                                   location=['form', 'json'],
                                   required=False)
speakerinfo_reqparser.add_argument('keynote_link', type=str, trim=True,
                                   location=['form', 'json'],
                                   nullable=True,
                                   help='No speakerinfo keynote_link provided')
speakerinfo_reqparser.add_argument('admin_approved', type=bool,
                                   location=['form', 'json'],
                                   required=False, nullable=True)

speakerinfo_reqparser.add_argument('title', type=str, trim=True,
                                   location=['form', 'json'],
                                   required=False, nullable=False,
                                   help='No speakerinfo title provided')
speakerinfo_reqparser.add_argument('description', type=str, trim=True,
                                   location=['form', 'json'],
                                   required=False, nullable=False,
                                   help='No speakerinfo description provided')


class SpeakerInfoListResource(Resource):
    @marshal_with(speakerinfo_fields)
    def get(self):
        if not SigninManager.get_is_signed_in():
            raise SigninRequiredError("Signin required.")

        speakerinfo = SpeakerInfoRepo.get_with_user_id(
            SigninManager.get_user_id())

        if speakerinfo is None:
            speakerinfo = SpeakerInfo()

        return speakerinfo

    @marshal_with(speakerinfo_fields)
    def post(self):
        if not SigninManager.get_is_signed_in():
            raise SigninRequiredError("Signin required.")

        args = json.loads(request.data.decode("utf-8"))

        user_id = SigninManager.get_user_id()

        speakerinfo = SpeakerInfo.query.filter_by(user_id=user_id).first()

        if speakerinfo is None:
            speakerinfo = SpeakerInfoRepo.insert(args)
        else:
            speakerinfo.introduce = args["introduce"]
            speakerinfo.history = args["history"]
            speakerinfo.title = args["title"]
            speakerinfo.description = args["description"]
            speakerinfo.keynote_link = args["keynote_link"]

            try:
                db.session.merge(speakerinfo)
                db.session.commit()
            except IntegrityError as e:
                print(str(e))
                db.session.rollback()
                abort_with_integrityerror(e)
            except Exception as e:
                print(str(e))
                db.session.rollback()
                raise e

        return speakerinfo


class SpeakerInfoResource(Resource):
    @marshal_with(speakerinfo_fields)
    def get(self, pk):
        if not CredentialManager.get_is_admin():
            raise UnauthorizedError("Unauthorized.")

        speakerinfo = get_or_404(SpeakerInfo, pk)

        return speakerinfo

    @marshal_with(speakerinfo_fields)
    def put(self, pk):
        args = speakerinfo_reqparser.parse_args()

        speakerinfo = get_or_404(SpeakerInfo, pk)

        speakerinfo = SpeakerInfoRepo.update(speakerinfo, args)

        return speakerinfo

    def delete(self, pk):
        if not CredentialManager.get_is_admin():
            raise UnauthorizedError("Unauthorized.")

        speakerinfo = get_or_404(SpeakerInfo, pk)
        SpeakerInfoRepo.delete(speakerinfo)

        return '', 204


speaker_api = Blueprint('resources.speakerinfos', __name__)
api = Api(speaker_api)
api.add_resource(
    SpeakerInfoListResource,
    '',
    endpoint='speakerinfos'
)

api.add_resource(
    SpeakerInfoResource,
    '/<int:pk>',
    endpoint='speakerinfo'
)
