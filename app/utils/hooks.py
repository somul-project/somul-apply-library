import json

from flask import request
from flask import session

from app.managers.signin import (SESSIONKEY_IS_SIGNED_IN,
                                 SESSIONKEY_USER_ID)
from app.utils.loggers import log_request


def _convert_to_log_object(_session, _request):
    log_object = {}
    log_object["base_url"] = _request.base_url

    _log_session = {}
    session_args = [
        SESSIONKEY_IS_SIGNED_IN,
        SESSIONKEY_USER_ID
    ]
    for arg in session_args:
        _log_session[arg] = session[arg]

    log_object["session"] = _log_session

    log_object["headers"] = request.headers.to_list()

    request_args = [
        "cookies",
        "access_route",
        "user_agent",
        "query_string",
        "args",
        "values",
        "is_json",
        "json",
    ]

    _log_req = {}
    for arg in request_args:
        _log_req[arg] = getattr(_request, arg)
        try:
            json.dumps(_log_req[arg])
        except Exception as e:
            _log_req[arg] = str(_log_req[arg])

    log_object["request"] = _log_req

    return log_object


def add_before_and_after_hook(app):
    @app.before_request
    def before_request():
        request_log = _convert_to_log_object(session, request)
        if log_request(request_log):
            print(request_log)
        else:
            print("Fail")

    @app.after_request
    def after_request(response):
        print("after")
        ## headers
        # Content-Type: application/json
        # Content-Length: 82
        ## status
        #  '400 BAD REQUEST'
        ## status_code
        # 400
        ## data
        # b'{\n    "message": "Duplicate entry \'swe.jaeyoungpark@gmail.com\' for key \'email\'"\n}\n'
        ## content_type
        # 'application/json'
        session[SESSIONKEY_IS_SIGNED_IN]
        session[SESSIONKEY_USER_ID]

        return response
