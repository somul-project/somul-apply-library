from flask import Blueprint
from flask_restful import (Resource, fields, marshal_with,
                           Api)
from sqlalchemy.exc import IntegrityError

from app.database import db, get_or_404
from app.database.models import SpeakerInfo
from app.utils.errors import abort_with_integrityerror, UnauthorizedError
from app.managers.credential import CredentialManager

speaker_fields = {
    '_id': fields.Integer,
    'user_id': fields.Integer,
    'session_time': fields.String,
    'introduce': fields.String,
    'history': fields.String,
    'keynote_link': fields.String,
    'admin_approved': fields.String
}


class AdminApproveResource(Resource):
    @marshal_with(speaker_fields)
    def get(self, pk):
        if not CredentialManager.get_is_admin():
            raise UnauthorizedError("Unauthorized.")

        speaker = get_or_404(SpeakerInfo, pk)

        speaker.admin_approved = 0

        try:
            db.session.merge(speaker)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            abort_with_integrityerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return {
            "result": 0
        }


class AdminRejectResource(Resource):
    def get(self, pk):
        if not CredentialManager.get_is_admin():
            raise UnauthorizedError("Unauthorized.")

        speaker = get_or_404(SpeakerInfo, pk)

        speaker.admin_approved = 1

        try:
            db.session.merge(speaker)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            abort_with_integrityerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return {
            "result": 0
        }


admin_api = Blueprint('resources.admin', __name__)
api = Api(admin_api)
api.add_resource(
    AdminApproveResource,
    '/approve/<int:pk>',
    endpoint='approve'
)

api.add_resource(
    AdminRejectResource,
    '/reject/<int:pk>',
    endpoint='reject'
)
