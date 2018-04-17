from flask import Blueprint
from flask_restful import (Resource, reqparse, fields,
                           marshal_with, Api)

from app.database import get_or_404
from app.database.models import SpeakerInfo
from app.database.speakerinfo import SpeakerInfoRepo
from app.managers.credential import CredentialManager
from app.managers.signin import SigninManager
from app.utils.errors import UnauthorizedError, SigninRequiredError

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
                                   required=False, nullable=False,
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

        args = speakerinfo_reqparser.parse_args()

        speakerinfo = SpeakerInfoRepo.get_with_user_id(
            SigninManager.get_user_id())

        if speakerinfo is None:
            speakerinfo = SpeakerInfoRepo.insert(args)
        else:
            speakerinfo = SpeakerInfoRepo.update(speakerinfo, args)

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

class SpeakerInfoBySignResource(Resource):
    def post(self):
        args = speakerinfo_reqparser.parse_args()
        pk = SigninManager.get_user_id()
        speakerinfo = get_or_404(SpeakerInfo, pk)
        SpeakerInfoRepo.update(speakerinfo, args)

        return {
            "result": 0
        }


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

api.add_resource(
    SpeakerInfoBySignResource,
    '/modify'
)