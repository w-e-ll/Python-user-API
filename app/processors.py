"""
This module implements general workflow of requested operation.
All interfaces implemented on 'Pure Python Objects'.
This module does not handle errors. All handling should be implemented
by caller. All exceptions goes to outer scope.
"""
import json

from typing import (
    Tuple, List, Dict,
    Union, Any, Optional,
    Iterable, MutableMapping
)
from uuid import uuid4

from scripts import get_digest
from db_adaptor import (
    update_user, find_one_by_filter,
    find_one_by_email, insert_user,
    insert_users, count_tot_users, get_users
)


def process_list_users() -> Dict[str, Any]:
    """Returns total users from Users collection. Counts result."""
    count_users = count_tot_users()
    users_list = get_users()

    users_collection = {
        'usersCount': count_users,
        'totalUsers': users_list,
    }
    return users_collection


def process_update_user(user_uuid: str,
                        new_user: Dict[Union[str, int], Any],
                        keys_to_digest: List[str]) \
                        -> Optional[Dict[Union[str, int], Any]]:
    """Updates user by given fields. Searches by uuid."""
    obj_to_digest = {key: value
                     for key, value in new_user.items()
                     if key in keys_to_digest}
    new_digest: str = get_digest(json.dumps(obj_to_digest))

    # Update a user and return
    user_to_db = {key: value
                  for key, value in new_user.items()
                  if key in keys_to_digest}
    user_to_db['uuid'] = user_uuid
    user_to_db['digest'] = new_digest
    updated_user = update_user(user_uuid, user_to_db)
    return updated_user


def process_post_user(user_to_create: Dict[Union[str, int], Any],
                      fields_to_digest: List[str]) \
        -> Tuple[bool, Union[str, Optional[Dict[Union[str, int], Any]]]]:
    """Adds only one user to collection"""
    user_email = user_to_create.get('email')
    exists = find_one_by_filter({'email': user_email})
    if exists:
        new: bool = False
        return new, f"User with email: {user_email}, is in the DB."

    # If same digest in the DB, then return this record.
    required_fields_digest = {key: value
                              for key, value in
                              user_to_create.items()
                              if key in fields_to_digest}
    digest: str = get_digest(json.dumps(required_fields_digest))

    # Insert a record in DB then return user
    required_fields_digest['uuid'] = 'USER-' + uuid4().hex.upper()
    required_fields_digest['digest'] = digest
    user_id: str = insert_user(required_fields_digest)
    created_user = find_one_by_filter({'_id': user_id})
    new = True
    return new, created_user


def process_post_users(users_to_add: Iterable[Dict[Union[str, int], Any]],
                       fields_to_digest: List[str]) \
                       -> Tuple[bool, Union[str, List[str]]]:
    """ Adds new users to Users collection."""
    new_users_emails = [user['email'].lower() for user in users_to_add]
    known_emails = [find_one_by_email({'email': user_email})
                    for user_email in new_users_emails]
    unknown_emails = set(new_users_emails) ^ set(known_emails)

    if not unknown_emails:
        new = False
        return new, "No new users, nothing to add."

    # if we have new emails, - collect users
    users_to_insert: List[MutableMapping[Any, Any]] = []
    for user in users_to_add:
        if user['email'] in unknown_emails:
            # If same digest in the DB then return this record
            required_fields_digest = {key: value
                                      for key, value in user.items()
                                      if key in fields_to_digest}
            digest: str = get_digest(json.dumps(required_fields_digest))
            # Insert a record in DB then return this record
            required_fields_digest['uuid'] = 'USER-' + uuid4().hex.upper()
            required_fields_digest['digest'] = digest
            users_to_insert.append(required_fields_digest)
    # if we have new users, - insert
    result = insert_users(users_to_insert)
    new = True
    return new, result
