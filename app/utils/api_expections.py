"""
重构 http exception
"""
import json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 400
    message = ''

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code
        self.description = self.message

        super(APIException, self).__init__(self.message, None)

    def __str__(self):
        if not self.code:
            self.code = 400
        result = {
            "code": self.code,
            "message": self.message
        }
        return json.dumps(result)

    def __repr__(self):
        code = self.code if self.code is not None else '???'
        return "<%s '%s: %s'>" % (self.__class__.__name__, code, self.name)

    def get_body(self, environ=None, scope=None):
        return self.__str__()

    def get_headers(self, environ=None, scope=None):
        return [('Content-Type', 'application/json')]


class ParameterValidationFailed(APIException):
    code = 400
    error = 'ParameterValidationFailed'
    message = 'Parameter Validation Failed'

    def __init__(self, message=None):
        super(ParameterValidationFailed, self).__init__(message=message)


class RequestMethodError(APIException):
    code = 405
    error = 'RequestMethodError'
    message = 'Request Method Not Allowed'

    def __init__(self, message=None):
        super(RequestMethodError, self).__init__(message=message)


class RequestInvalidParams(APIException):
    code = 400
    error = 'InvalidParams'
    message = 'Invalid Params'

    def __init__(self, message=None):
        super(RequestInvalidParams, self).__init__(message=message)


class QueryParamsTooLong(APIException):
    code = 414
    error = 'QueryParamsTooLong'
    message = 'Query Params Too Long'

    def __init__(self, message=None):
        super(QueryParamsTooLong, self).__init__(message=message)


class RequestEntityTooLarge(APIException):
    code = 414
    error = 'RequestEntityTooLarge'
    message = 'Request Entity Too Large'

    def __init__(self, message=None):
        super(RequestEntityTooLarge, self).__init__(message=message)


class URLNotFound(APIException):
    code = 404
    error = 'URLNotFound'
    message = 'URL Not Found'

    def __init__(self, message=None):
        super(URLNotFound, self).__init__(message=message)


class InternalServerError(APIException):
    code = 500
    error = 'InternalServerError'
    message = 'Internal Server Error'

    def __init__(self, message=None):
        super(InternalServerError, self).__init__(message=message)
