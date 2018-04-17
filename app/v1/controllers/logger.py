from flask import Blueprint
from flask_restful import Resource, Api

from app.database.logger_models import Log
from app.utils.errors import UnauthorizedError
from app.managers.credential import CredentialManager
from app.utils.hooks import donot_stack_log


class LoggerResource(Resource):
    def get(self):
        if not CredentialManager.get_is_admin():
            raise UnauthorizedError("Unauthorized.")

        logs = Log.query.order_by(Log._id.desc()).all()

        results = []
        for item in logs:
            results.append({
                "_id": item._id,
                "type": item.logtype,
                "content": item.content,
                "created_at": str(item.created_at),
            })

        return results


logger_api = Blueprint('resources.logger', __name__)
donot_stack_log(logger_api)

api = Api(logger_api)
api.add_resource(
    LoggerResource,
    '',
)
