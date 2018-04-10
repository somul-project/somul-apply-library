from werkzeug.exceptions import HTTPException


class InvalidArgumentError(HTTPException):
    code = 400


class DataNotFoundError(HTTPException):
    code = 404


class DuplicatedDataError(HTTPException):
    code = 400


class WrongSecretkeyError(HTTPException):
    code = 400
