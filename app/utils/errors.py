from werkzeug.exceptions import HTTPException


class InvalidArgumentError(HTTPException):
    code = 400


class DataNotFoundError(HTTPException):
    code = 404


class DuplicatedDataError(HTTPException):
    code = 400


class InvalidRelationDataError(HTTPException):
    code = 400


class UnknownDataError(HTTPException):
    code = 400


class WrongSecretkeyError(HTTPException):
    code = 400


class UnauthorizedError(HTTPException):
    code = 400


class UserDoesntExistsError(HTTPException):
    code = 400


class UserPasswordIncorrectError(HTTPException):
    code = 400


class SigninRequiredError(HTTPException):
    code = 400


class UserSessionEmptyError(HTTPException):
    code = 400

class EmailNotSendedError(HTTPException):
    code = 400


def abort_with_integrityerror(e):
    if e.orig.args[0] == 1452:
        raise InvalidRelationDataError(str(e.orig.args[1]))
    elif e.orig.args[0] == 1062:
        raise DuplicatedDataError(str(e.orig.args[1]))

    raise UnknownDataError(str(e.orig))
