from werkzeug.exceptions import HTTPException


class DataNotFoundError(HTTPException):
    code = 404


class DuplicatedDataError(HTTPException):
    code = 400
