import yaml
import json
import hashlib

from bottle import Response, BaseResponse
from bson import json_util
from typing import Union, Dict, Any, Optional

import errors
import config
from logger_setup import logger

AnyExcCls = Union[
    Exception, errors.InternalServerError, errors.BadRequestBody,
    errors.UserNotFound, errors.ContentTypeError,
    errors.AcceptTypeError, errors.WrongMethod
]


def get_swagger_docs():
    """
    summary: Sends API documentation to endpoints
    """
    with open('static/swagger.json', 'r') as file:
        swagger_json = json.load(file)
    return json.dumps(swagger_json)


def load_swagger_yaml():
    """
    summary: Loads swagger yaml file.
    description: Swagger specification documentation.
    """
    with open('static/swagger.yaml') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_definitions_yaml():
    """
    summary: Loads definitions yaml file.
    description: Swagger validation definitions.
    """
    with open('static/definitions.yaml') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def log_exception(e: AnyExcCls) -> Any:
    # Log_exception by Logging module.
    return logger.exception(e)


def json_response(obj: Any, status: int = 200,
                  headers: Optional[dict] = None) -> BaseResponse:
    """Makes right json response message."""
    json_text = json_util.dumps(obj, indent=2,
                                sort_keys=True,
                                ensure_ascii=False)
    return Response(body=json_text, content_type='application/json',
                    status=status, headers=headers)


def json_error_response(e: AnyExcCls) -> BaseResponse:
    if not isinstance(e, errors.ServerError):
        raise RuntimeError('Only ServerError type is accepted!')
    error_object = construct_error_object(e.name_json,
                                          e.debug_id_json,
                                          e.message_json,
                                          e.information_link_json,
                                          e.links_json)
    return json_response(error_object, status=e.status_code)


def construct_error_object(name: str, debug_id: str, message: str,
                           information_link: Optional[str] = None,
                           links: Optional[str] = None) -> Dict[str, str]:
    error_json = {
        'name': name,
        'debug_id': debug_id,
        'message': message
    }

    if information_link:
        error_json['information_link'] = information_link
    if links:
        error_json['links'] = links
    return error_json


def get_digest(message: str) -> str:
    """
    Returns message auth code as a base64 encoded string
    """
    digest_alg = hashlib.new('sha1')
    message_as_bytes = bytes(message, 'utf-8')
    digest_alg.update(message_as_bytes)
    return digest_alg.hexdigest()


def uuid_filter(config):
    """
    Provides a Bottle routing filter for UUIDs
    """
    regexp = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

    def to_python(match):
        return match

    def to_url(ext):
        return ext

    return regexp, to_python, to_url
