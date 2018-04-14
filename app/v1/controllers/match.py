from flask import Blueprint
from flask_restful import (Resource, reqparse, Api)
from sqlalchemy.exc import IntegrityError

from app.database import db, get_or_404
from app.database.models import Library, User
from app.managers.signin import SigninManager
from app.utils.errors import abort_with_integrityerror


class MatchVolunteerResource(Resource):
    def get(self, pk):
        # TODO(@harrydrippin) Signin Check
        library = get_or_404(Library, pk)
        user_list = list()
        for user in library.users:
            if not user.speakerinfos:
                user_list.append(user)

        if len(user_list) >= 2:
            return {
                "result": 1,
                "cause": "이미 정원이 꽉 찼습니다."
            }
        user_id = SigninManager.get_user_id()
        user = get_or_404(User, user_id)

        # TODO(@harrydrippin): Check if ref exist above this situation
        user.library_id = library._id

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

        return {
            "result": 0
        }


matchspeaker_reqparser = reqparse.RequestParser()
matchspeaker_reqparser.add_argument("time", type=str, trim=True,
                                    location=['args'], required=True,
                                    nullable=False,
                                    help="No time information provided")


class MatchSpeakerResource(Resource):
    def get(self, pk):
        # TODO(@harrydrippin) Signin Check
        library = get_or_404(Library, pk)
        user_list = library.users

        args = matchspeaker_reqparser.parse_args()
        session_time = list()
        for user in user_list:
            # TODO(@harrydrippin): Verify that below if line works
            if user.speakerinfos:
                speaker_info = user.speakerinfos
                session_time.append(speaker_info.session_time)

        if session_time.count(args["time"]) != 0:
            return {
                "result": 1,
                "cause": "이미 할당된 세션입니다. 다른 세션을 선택해주세요."
            }

        user_id = SigninManager.get_user_id()
        user = get_or_404(User, user_id)

        user.speakerinfos.session_time = args["time"]

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

        return {
            "result": 0
        }


match_api = Blueprint('resources.match', __name__)
api = Api(match_api)
api.add_resource(
    MatchVolunteerResource,
    '/volunteer/<int:pk>',
    endpoint='libraries'
)

api.add_resource(
    MatchSpeakerResource,
    '/speaker/<int:pk>',
    endpoint='library'
)
