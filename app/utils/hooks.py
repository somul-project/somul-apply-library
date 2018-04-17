import json

from flask import request, session

from app.managers.signin import (SESSIONKEY_IS_SIGNED_IN,
                                 SESSIONKEY_USER_ID)
from app.utils.loggers import log_request, log_response


ALLOWED_REQUEST_HOOK = []


def _convert_session_to_log_object():
    _log_session = {}
    session_args = [
        SESSIONKEY_IS_SIGNED_IN,
        SESSIONKEY_USER_ID
    ]
    for arg in session_args:
        if hasattr(session, arg):
            _log_session[arg] = session[arg]

    return _log_session


def _convert_request_to_log_object(_request):
    log_object = {}
    log_object["session"] = _convert_session_to_log_object()
    log_object["headers"] = _request.headers.to_list()
    log_object["base_url"] = _request.base_url

    request_args = [
        "cookies",
        "access_route",
        "user_agent",
        "query_string",
        "args",
        "values",
        "is_json",
        "json",
        "form",
    ]

    _log_req = {}
    for arg in request_args:
        if hasattr(_request, arg):
            _log_req[arg] = getattr(_request, arg)
            try:
                json.dumps(_log_req[arg])
            except Exception:
                _log_req[arg] = str(_log_req[arg])

    log_object["request"] = _log_req

    return log_object


def _convert_response_to_log_object(_response):
    log_object = {}
    log_object["session"] = _convert_session_to_log_object()

    response_args = [
        "headers",
        "status",
        "status_code",
        "data",
        "content_type",
    ]

    _log_res = {}
    for arg in response_args:
        if hasattr(_response, arg):
            _log_res[arg] = getattr(_response, arg)
            try:
                json.dumps(_log_res[arg])
            except Exception:
                _log_res[arg] = str(_log_res[arg])

    log_object["response"] = _log_res

    return log_object


def add_before_and_after_hook(app):
    @app.before_request
    def before_request():
        try:
            if request.blueprint not in ALLOWED_REQUEST_HOOK:
                return

            request_log = _convert_request_to_log_object(request)
            if not log_request(request_log):
                print("log_request Fail")
        except Exception as e:
            print("log_request Fail, e = " + str(e))

    @app.after_request
    def after_request(response):
        try:
            if request.blueprint not in ALLOWED_REQUEST_HOOK:
                return response

            response_log = _convert_response_to_log_object(response)
            if not log_response(response_log):
                print("log_response Fail")

        except Exception as e:
            print("log_request Fail, e = " + str(e))

        return response


def add_request_hook(api):
    from flask import Blueprint
    if isinstance(api, Blueprint):
        ALLOWED_REQUEST_HOOK.append(api.name)
