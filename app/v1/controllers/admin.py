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
    'introduce': fields.Text,
    'history': fields.Text,
    'keynote_link': fields.String,
    'admin_approved': fields.String
}


class AdminApproveResource(Resource):
    @marshal_with(speaker_fields)
    def get(self, pk):
        if not CredentialManager.get_is_admin():
            raise UnauthorizedError("Unauthorized.")

        speaker = get_or_404(SpeakerInfo, pk)

        speaker.admin_approved = True

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

        return speaker


class AdminRejectResource(Resource):
    def get(self, pk):
        if not CredentialManager.get_is_admin():
            raise UnauthorizedError("Unauthorized.")

        speaker = get_or_404(SpeakerInfo, pk)

        speaker.admin_approved = False

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

        return speaker


admin_api = Blueprint('resources.maps', __name__)
api = Api(admin_api)
api.add_resource(
    AdminApproveResource,
    '/approve/<int:pk>',
    endpoint='admin'
)

api.add_resource(
    AdminApproveResource,
    '/reject/<int:pk>',
    endpoint='admin'
)
