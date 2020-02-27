"""
This module processes HTTP request and sends HTTP responses.
"""
import os

from bottle import (
    static_file, template, request,
    Response, BaseResponse,
)
from typing import Union, Optional, Tuple, Any

from db_adaptor import (
    count_tot_users, find_one_by_email,
    read_by_uuid, delete_by_uuid, make_drop
)
import errors
from config import (
    SUPPORTED_METHODS
)
from processors import (
    process_list_users, process_update_user,
    process_post_user, process_post_users
)
from validators import (
    validate_request_headers,
    validate_user_uuid,
    validate_json_object,
    validate_request_method,
    validate_user_email
)
from scripts import (
    log_exception,
    json_error_response,
    json_response,
    load_definitions_yaml
)


def get_spec_digest() -> Tuple[Any, Any]:
    """Get swagger spec, user_obj, keys_to_digest"""
    swagger_spec = request.app.config['api.swagger_spec']
    user_obj_spec = swagger_spec['definitions']['User']
    keys_to_digest = user_obj_spec['required']
    return keys_to_digest, user_obj_spec


def serve_static(filename: str) -> static_file:
    """Serves to filenames from static folder."""
    my_root = os.path.join(os.getcwd(), 'static')
    return static_file(filename, root=my_root)


definitions = load_definitions_yaml()


def index() -> template:
    """Front page of the API."""
    data = {"developer_name": "Valentin Sheboldaev",
            "developer_organization": "[W]NETWorks"}
    return template('index', data=data)


def validate_request(headers, method, supported_methods):
    """Validation of requested headers, method, supported_methods"""
    try:
        validate_request_method(method, supported_methods)
        validate_request_headers(headers)
    except errors.WrongMethod as e:
        e.message_json = e.message_json.format(method, supported_methods)
        log_exception(e)
        return json_error_response(e)
    except errors.AcceptTypeError as e:
        log_exception(e)
        return json_error_response(e)
    except errors.ContentTypeError as e:
        log_exception(e)
        return json_error_response(e)


def by_uuid(user_uuid: str) -> Union[Response, None]:
    """
      tags:
        - userAPI
      summary: Get's a single user record
      description: Get single user record by given user_uuid
      parameters:
        - name: user_uuid
          in: path
          description: UUID of the user to get
          required: true
          type: string
      responses:
        '200':
          description: OK
        '400':
          description: Validation error
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: User not found
          schema:
            $ref: '#/definitions/Error'
        '405':
          description: Wrong method
          schema:
            $ref: '#/definitions/Error'
        '406':
          description: >-
            Accept header is provided but 'application/json' type is not present
            in header
          schema:
            $ref: '#/definitions/Error'
        '415':
          description: >-
            Unsupported media type. 'Content-Type' header is provided and it is
            not the 'application/json'
          schema:
            $ref: '#/definitions/Error'
    """
    validate_request(
        request.headers, request.method,
        SUPPORTED_METHODS['/get_user_by_uuid']
    )
    try:  # Validate the UUID parameter
        validate_user_uuid(user_uuid)
    except errors.BadRequestQuery as e:
        e.message_json = f'Wrong user UUID: {user_uuid}'
        log_exception(e)
        return json_error_response(e)

    if request.method == 'GET':
        try:
            user = read_by_uuid(user_uuid)
            return json_response(user)
        except errors.UserNotFound as e:
            e.message_json = f'User with this ' \
                             f'{user_uuid} was not found.'
            log_exception(e)
            return json_error_response(e)
        except errors.InternalServerError as e:
            log_exception(e)
            return json_error_response(e)


def by_email(user_email: str) -> Union[Response, None]:
    """
      tags:
        - userAPI
      summary: Get's a single user record
      description: Get single user record by given user_email
      parameters:
        - name: user_email
          in: path
          description: Email of the user to get
          required: true
          type: string
      responses:
        '200':
          description: OK
        '400':
          description: Validation error
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: User not found
          schema:
            $ref: '#/definitions/Error'
        '405':
          description: Wrong method
          schema:
            $ref: '#/definitions/Error'
        '406':
          description: >-
            Accept header is provided but 'application/json' type is not present
            in header
          schema:
            $ref: '#/definitions/Error'
        '415':
          description: >-
            Unsupported media type. 'Content-Type' header is provided and it is
            not the 'application/json'
          schema:
            $ref: '#/definitions/Error'
    """
    validate_request(
        request.headers, request.method,
        SUPPORTED_METHODS['/get_user_by_email']
    )
    try:  # Validate the email parameter
        validate_user_email(user_email)
    except errors.BadRequestQuery as e:
        e.message_json = f'Wrong user email: {user_email}'
        log_exception(e)
        return json_error_response(e)

    if request.method == 'GET':
        try:
            user = find_one_by_email({'email': user_email})
            return json_response(user)
        except errors.UserNotFound as e:
            e.message_json = f'User with this ' \
                             f'{user_email} was not found.'
            log_exception(e)
            return json_error_response(e)
        except errors.InternalServerError as e:
            log_exception(e)
            return json_error_response(e)


def count_users() -> Union[int, None, Response]:
    """Implements GET logic of '/count_users' endpoint"""
    validate_request(
        request.headers, request.method,
        SUPPORTED_METHODS['/count_users']
    )

    if request.method == 'GET':
        try:  # Count users
            result = count_tot_users()
            return json_response(result)
        except errors.InternalServerError as e:
            e.message_json = 'Error while executing count'
            return json_error_response(e)


def get_total_users() -> BaseResponse:
    """
      tags:
        - userAPI
      summary: Get all system users
      responses:
        '200':
          description: OK
        '405':
          description: Wrong method
          schema:
            $ref: '#/definitions/Error'
        '406':
          description: >-
            Accept header is provided but 'application/json' type is not present
            in header
          schema:
            $ref: '#/definitions/Error'
        '415':
          description: >-
            Unsupported media type. 'Content-Type' header is provided and it is
            not the 'application/json'
          schema:
            $ref: '#/definitions/Error'
    """
    validate_request(  # validation of headers and method
        request.headers, request.method,
        SUPPORTED_METHODS['/get_total_users']
    )

    if request.method == 'GET':
        try:  # Get all system users
            users_list = process_list_users()
            return json_response(users_list)
        except errors.InternalServerError as e:
            e.message_json = 'Error while executing find_cursor.'
            return json_error_response(e)


def post_user() -> Optional[BaseResponse]:
    """
      tags:
        - userAPI
      summary: Adds a single user record
      parameters:
        - in: body
          name: body
          description: User object
          required: true
          schema:
            $ref: '#/definitions/User'
      responses:
        '200':
          description: OK
        '400':
          description: Validation error
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: User not found
          schema:
            $ref: '#/definitions/Error'
        '405':
          description: Wrong method
          schema:
            $ref: '#/definitions/Error'
        '406':
          description: >-
            Accept header is provided but 'application/json' type is not present
            in header
          schema:
            $ref: '#/definitions/Error'
        '415':
          description: >-
            Unsupported media type. 'Content-Type' header is provided and it is
            not the 'application/json'
          schema:
            $ref: '#/definitions/Error'
    """
    validate_request(  # do the validation
        request.headers, request.method,
        SUPPORTED_METHODS['/post_user']
    )
    if request.method == 'POST':
        try:
            user_to_create = request.json
        except Exception as e:
            log_exception(e)
            return json_error_response(errors.BadRequestBody())

        try:  # Validate JSON schema
            keys_to_digest, user_obj_spec = get_spec_digest()
            validate_json_object(user_to_create, user_obj_spec)
        except errors.BadRequestBody as e:
            log_exception(e)
            return json_error_response(e)

        try:  # Process post user
            new, result = process_post_user(
                user_to_create, keys_to_digest
            )
            status = 201 if new else 200
            return json_response(result, status=status)
        except errors.InternalServerError as e:
            log_exception(e)
            return json_error_response(e)


def post_users() -> Union[BaseResponse, None]:
    """
      tags:
        - userAPI
      summary: Adds users to User db. Upload as many as you want.
      description: 'Add as many users to User db, as want.'
      parameters:
        - name: body
          in: body
          description: List of users to post
          required: true
          schema:
            $ref: '#/definitions/Users'
      responses:
        '200':
          description: OK
        '400':
          description: Validation error
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: User not found
          schema:
            $ref: '#/definitions/Error'
        '405':
          description: Wrong method
          schema:
            $ref: '#/definitions/Error'
        '406':
          description: >-
            Accept header is provided but 'application/json' type is not present
            in header
          schema:
            $ref: '#/definitions/Error'
        '415':
          description: >-
            Unsupported media type. 'Content-Type' header is provided and it is
            not the 'application/json'
          schema:
            $ref: '#/definitions/Error'
    """
    validate_request(  # do the validation
        request.headers, request.method,
        SUPPORTED_METHODS['/post_users']
    )

    if request.method == 'POST':
        try:  # Load JSON object
            users_to_create = request.json
        except Exception as e:
            log_exception(e)
            return json_error_response(errors.BadRequestBody())

        try:  # Validate JSON schema
            keys_to_digest, user_obj_spec = get_spec_digest()
            [validate_json_object(user, user_obj_spec)
             for user in users_to_create]
        except errors.BadRequestBody as e:
            log_exception(e)
            return json_error_response(e)

        try:  # Post users
            new, res = process_post_users(
                users_to_create, keys_to_digest
            )
            status = 201 if new else 200
            return json_response(res, status=status)
        except errors.InternalServerError as e:
            log_exception(e)
            return json_error_response(e)


def update_user(user_uuid: str) -> Union[BaseResponse, None]:
    """
      tags:
        - userAPI
      summary: Updates an existing user
      parameters:
        - name: user_uuid
          in: path
          description: UUID of user to update
          required: true
          type: integer
        - name: body
          in: body
          description: User object to update
          required: true
          schema:
            $ref: '#/definitions/User'
      responses:
        '200':
          description: OK
        '400':
          description: Validation error
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: User not found
          schema:
            $ref: '#/definitions/Error'
        '405':
          description: Wrong method
          schema:
            $ref: '#/definitions/Error'
        '406':
          description: >-
            Accept header is provided but 'application/json' type is not present
            in header
          schema:
            $ref: '#/definitions/Error'
        '415':
          description: >-
            Unsupported media type. 'Content-Type' header is provided and it is
            not the 'application/json'
          schema:
            $ref: '#/definitions/Error'
    """
    validate_request(  # do the validation
        request.headers, request.method,
        SUPPORTED_METHODS['/update_user']
    )
    try:  # Validate the UUID parameter
        validate_user_uuid(user_uuid)
    except errors.BadRequestQuery as e:
        e.message_json = f'Wrong user UUID: {user_uuid}'
        log_exception(e)
        return json_error_response(e)

    if request.method == 'PUT':
        # Request new user
        try:
            new_user = request.json
        except Exception as e:
            log_exception(e)
            return json_error_response(errors.BadRequestBody())

        try:  # Validate JSON schema
            keys_to_digest, user_obj_spec = get_spec_digest()
            validate_json_object(new_user, user_obj_spec)
        except errors.BadRequestBody as e:
            log_exception(e)
            return json_error_response(e)

        try:  # Update user
            updated_user = process_update_user(
                user_uuid, new_user, keys_to_digest)
            return json_response(updated_user)
        except errors.InternalServerError as e:
            log_exception(e)
            return json_error_response(e)


def delete_user(user_uuid: str):
    """
      tags:
        - userAPI
      summary: Delete a single user record
      description: Delete a user
      parameters:
        - name: user_uuid
          in: path
          description: UUID of the user to delete
          required: true
          type: string
      responses:
        '204':
          description: Delete is OK
        '404':
          description: User not found or already deleted
          schema:
            $ref: '#/definitions/Error'
        '405':
          description: Wrong method
          schema:
            $ref: '#/definitions/Error'
    """
    validate_request(  # do the validation
        request.headers, request.method,
        SUPPORTED_METHODS['/delete_user']
    )
    if request.method == 'DELETE':
        try:
            delete_by_uuid(user_uuid)
            return Response(status=204)
        except errors.UserNotFound as e:
            e.message_json = f'User {user_uuid} not found'
            log_exception(e)
            return json_error_response(e)
        except errors.InternalServerError as e:
            log_exception(e)
            return json_error_response(e)


def drop_collection() -> Union[BaseResponse, None]:
    """Drop collection endpoint."""
    validate_request(  # do the validation
        request.headers, request.method,
        SUPPORTED_METHODS['/drop_collection']
    )
    if request.method == 'POST':
        try:
            result = make_drop()
            return json_response(result, status=202)
        except errors.ExternalResource as e:
            e.message_json = 'External resource error ' \
                             'when dropping collection.'
            log_exception(e)
            return json_error_response(e)
        except errors.InternalServerError as e:
            e.message_json = 'Error while dropping collection.'
            log_exception(e)
            return json_error_response(e)
