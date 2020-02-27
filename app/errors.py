"""
This module contains all high level server errors.
"""
from uuid import uuid4


class ServerError(Exception):
    """
    Base class for all server errors.
    """
    pass


class UserNotFound(ServerError):
    """
    Implements 404 HTTP Not Found
    """
    def __init__(self, message=''):
        super().__init__(message)
        self.status_code = 404
        self.name_json = 'ERR_USER_NOT_FOUND'
        self.debug_id_json = str(uuid4())
        self.message_json = 'The User you are requesting ' \
                            'is not found or does not exist.'
        self.information_link_json = None
        self.links_json = None


class InternalServerError(ServerError):
    """
    Implements 500 Internal Server HTTP Error
    """
    def __init__(self, message=''):
        super().__init__(message)
        self.status_code = 500
        self.name_json = 'ERR_SERVER_INTERNAL'
        self.debug_id_json = str(uuid4())
        self.message_json = 'Internal server error. ' \
                            'No additional info will be provided.'
        self.information_link_json = None
        self.links_json = None


class RequestValidationError(ServerError):
    """
    Base class for request validators
    """
    pass


class BadRequest(RequestValidationError):
    """
    Implements 400 Bad Request Entity HTTP Error
    """
    def __init__(self, message=''):
        super().__init__(message)
        self.status_code = 400


class BadRequestBody(BadRequest):
    """
    Implements bad body error
    """
    def __init__(self, message=''):
        super().__init__(message)
        self.name_json = 'ERR_IN_BODY'
        self.debug_id_json = str(uuid4())
        self.message_json = 'You are requesting user ' \
                            'with a wrong body scheme.'
        self.information_link_json = None
        self.links_json = None


class BadRequestQuery(BadRequest):
    """
    Implements error in request query
    """
    def __init__(self, message=''):
        super().__init__(message)
        self.name_json = 'ERR_IN_QUERY'
        self.debug_id_json = str(uuid4())
        self.message_json = 'You are requesting user ' \
                            'with a wrong request parameters.'
        self.information_link_json = None
        self.links_json = None


class WrongMethod(RequestValidationError):
    """
    Implements error in request method
    """
    def __init__(self, message=''):
        super().__init__(message)
        self.status_code = 405
        self.name_json = 'ERR_HTTP_METHOD'
        self.debug_id_json = str(uuid4())
        self.message_json = 'You are requesting user with WrongMethod.'
        self.information_link_json = None
        self.links_json = None


class AcceptTypeError(RequestValidationError):
    """
    Implements error in Accept header field
    """
    def __init__(self, message=''):
        super().__init__(message)
        self.status_code = 406
        self.name_json = 'ERR_TYPE_NOT_SUPPORTED'
        self.debug_id_json = str(uuid4())
        self.message_json = 'Accept header is provided but ' \
                            'application/json is not requested. ' \
                            'Make a request with Accept: application/json'\
                            ' header or with no Accept header at all.'
        self.information_link_json = None
        self.links_json = None


class ContentTypeError(RequestValidationError):
    """
    Implements error in Content-Type header field
    """
    def __init__(self, message=''):
        super().__init__(message)
        self.status_code = 415
        self.name_json = 'ERR_UNSUPPORTED_MEDIA_TYPE'
        self.debug_id_json = str(uuid4())
        self.message_json = 'Content-Type header is provided but ' \
                            'application/json is not requested. Make a ' \
                            'request with Content-Type: application/json '\
                            'header or with no Content-Type header at all.'
        self.information_link_json = None
        self.links_json = None


class ExternalResource(ServerError):
    """
    Implements 422 Unprocessable Entity HTTP Error
    """
    def __init__(self, message=''):
        super().__init__(message)
        self.status_code = 422
        self.name_json = 'ERR_EXTERNAL_RESOURCE'
        self.debug_id_json = str(uuid4())
        self.message_json = 'The requested action cannot be performed.'
        self.information_link_json = None
        self.links_json = None
