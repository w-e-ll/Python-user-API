"""
This is a collection of different validators (request query, body, methods).
"""
import re
from jsonschema import validate, ValidationError
from typing import Dict, Union, Any, List

import errors
from config import (
    SUPPORTED_CONTENT_TYPE,
    UUID_MATCH_PATTERN
)
from scripts import log_exception


def validate_user_email(email: str):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not bool(re.search(regex, email)):
        raise ValueError()


def validate_accept_header(accept_header, supported_content_type):
    if supported_content_type not in accept_header.lower():
        raise errors.AcceptTypeError()


def validate_request_method(method, supported_methods):
    if method not in supported_methods:
        raise errors.WrongMethod()


def validate_request_headers(headers):
    accept_header = headers.get('Accept')
    if accept_header:
        validate_accept_header(accept_header, SUPPORTED_CONTENT_TYPE)

    content_type_header = headers.get('Content-Type')
    if content_type_header:
        validate_content_type_header(content_type_header,
                                     SUPPORTED_CONTENT_TYPE)


def validate_user_uuid(user_uuid: str):
    valid_user_uuid = bool(re.match(UUID_MATCH_PATTERN, user_uuid))
    if not valid_user_uuid:
        raise errors.BadRequestQuery()


def validate_content_type_header(content_type_header,
                                 supported_content_type):
    if supported_content_type not in content_type_header.lower():
        raise errors.ContentTypeError()


def validate_json_object(obj: Dict[Union[str, int], Any],
                         spec: List[str]) -> validate:
    try:
        validate(obj, spec)
    except ValidationError as e:
        log_exception(e)
        raise errors.BadRequestBody()
