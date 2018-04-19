import json

from flask import Blueprint
from flask_restful import Resource, Api

from app.database.logger_models import Log
from app.utils.errors import UnauthorizedError
from app.managers.credential import CredentialManager


def cleanup_rawbytestr(raw_data):
    special_charactor_removed = raw_data \
        .replace("\\n", "") \
        .replace("\\\\", "\\") \
        .replace("b'[", "[") \
        .replace("]'", "]")
    return special_charactor_removed


def raw_logitem_to_dict(logitem):
    result = {}

    fields = [
        "_id",
        "logtype",
        "created_at",
        "content",
    ]

    for field in fields:
        result[field] = getattr(logitem, field)

    content = json.loads(logitem.content)
    if "response" in content:
        content["response"]["data"] = \
            json.loads(cleanup_rawbytestr(content["response"]["data"]))

    result["content"] = content

    return result



class LoggerResource(Resource):
    def get(self):
        if not CredentialManager.get_is_admin():
            raise UnauthorizedError("Unauthorized.")

        logs = Log.query.order_by(Log._id.desc()).all()

        results = []
        for item in logs:
            results.append(raw_logitem_to_dict(item))

        return results


logger_api = Blueprint('resources.logger', __name__)

api = Api(logger_api)
api.add_resource(
    LoggerResource,
    '',
)
