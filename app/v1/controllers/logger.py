import json

from flask import Blueprint
from flask_restful import Resource, Api

from app.database.logger_models import Log
from app.utils.errors import UnauthorizedError
from app.managers.credential import CredentialManager


def cleanup_rawbytestr(raw_data):
    raw_data = raw_data[2:-1]
    raw_data = raw_data.replace('\\"', '"')
    raw_data = raw_data.replace("\\'", "'")
    raw_data = raw_data.replace('\\\\n', "")
    raw_data = raw_data.replace('\\n', "")

    return raw_data


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
        cleanedup_rawbytestr = cleanup_rawbytestr(content["response"]["data"])
        content["response"]["data"] = \
            json.loads(cleanedup_rawbytestr)

    result["content"] = content
    result["created_at"] = str(result["created_at"])

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
