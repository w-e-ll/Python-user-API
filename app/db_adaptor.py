"""
This module is responsible for high and low level database operations.
"""
from typing import (
    List, Dict, Union, Iterable,
    Any, Iterator, Optional,
    MutableMapping
)
from pymongo import results
from pymongo import MongoClient
from pymongo import ReturnDocument

import errors
from config import DATABASE
from scripts import log_exception

DB_HOST = DATABASE['ADDRESS']
DB_PORT = DATABASE['PORT']
DB_NAME = DATABASE['DB_NAME']
COLLECTION_NAME = DATABASE['COL_NAME']


class DBAdapter:
    """
    This is a high level adapter over MongoDB.
    Low level methods mimics PyMongo function names.
    Database client and database objects are singletons (Borg actually).
    """
    def __init__(self):
        self._client = MongoClient(DB_HOST, DB_PORT)
        self._db = self._client[DB_NAME]
        self._col_name = COLLECTION_NAME

    def drop(self) -> Optional[Iterable[str]]:
        self._db[self._col_name].drop()
        return self._db.list_collection_names()

    def insert_many(self, to_insert: List[MutableMapping[Any, Any]]) \
            -> results.InsertManyResult:
        return self._db[self._col_name].insert_many(to_insert)

    def insert_one(self, to_insert: MutableMapping[Any, Any]) \
            -> results.InsertOneResult:
        return self._db[self._col_name].insert_one(to_insert)

    def delete_one(self, delete_filter: Dict[Union[str, int], Any]) \
            -> results.DeleteResult:
        return self._db[self._col_name].delete_one(delete_filter)

    def count(self) -> Optional[int]:
        return self._db[self._col_name].count()

    def find_cursor(self, **kwargs) -> Iterator:
        cursor_iter = self._db[self._col_name].find(**kwargs)
        return cursor_iter

    def find_one(self,
                 filter_q: Dict[Union[str, int], Any], *args, **kwargs) \
            -> Optional[Dict[Union[str, int], Any]]:
        return self._db[self._col_name].find_one(filter_q, *args, **kwargs)

    def find_one_and_update(self, search_filter: Dict[Union[str, int], Any],
                            update: Dict[Union[str, int], Any], **kwargs) \
            -> Optional[Dict[Union[str, int], Any]]:
        return self._db[self._col_name].find_one_and_update(
            search_filter, update, **kwargs
        )


def get_db_adaptor():
    """
    A factory to get a DBAdapter object
    """
    return DBAdapter()


def get_users() -> List[Dict[Union[str, int], Any]]:
    """
    Returns list of user objects from users collection.
    Raises errors.InternalServerError is any other errors.
    """
    try:
        db_adaptor = get_db_adaptor()
        return [i for i in db_adaptor.find_cursor()]
    except Exception as e:
        log_exception(e)
        raise errors.InternalServerError()


def make_drop() -> Optional[Iterable[str]]:
    """
    Drops users collection.
    Raises errors.InternalServerError
    is any errors.
    """
    try:
        db_adaptor = get_db_adaptor()
        return db_adaptor.drop()
    except Exception as e:
        log_exception(e)
        raise errors.InternalServerError()


def delete_by_uuid(user_uuid: str):
    """
    Deletes user from collection given by user_uuid.
    Raises errors.InternalServerError is any errors.
    """
    try:
        # Check that user is actually present
        db_adaptor = get_db_adaptor()
        user = db_adaptor.find_one({'uuid': user_uuid},
                                   projection={'_id': False})
        if user is None:
            raise errors.UserNotFound()

        # Delete user
        result = db_adaptor.delete_one({'uuid': user_uuid})
        if not result.acknowledged:
            raise errors.InternalServerError()
        return result
    except Exception as e:
        log_exception(e)
        raise errors.InternalServerError()


def read_by_uuid(user_uuid: str) -> Optional[Dict[Union[str, int], Any]]:
    """
    Get user obj from collection by given user_uuid.
    Raises errors.UserNotFound if user is not found by user_uuid.
    Raises errors.InternalServerError is any other errors.
    """
    try:
        db_adaptor = get_db_adaptor()
        return db_adaptor.find_one({'uuid': user_uuid},
                                   projection={'_id': False})
    except errors.UserNotFound as e:
        log_exception(e)
        raise
    except Exception as e:
        log_exception(e)
        raise errors.InternalServerError()


def count_tot_users() -> Optional[int]:
    """
    Returns current size of Users collection.
    Raises errors.InternalServerError is any other errors.
    """
    try:
        db_adaptor = get_db_adaptor()
        return db_adaptor.count()
    except Exception as e:
        log_exception(e)
        raise errors.InternalServerError()


def insert_user(required_fields_digest: MutableMapping[Any, Any]) -> str:
    """Inserts one user to users collection. Returns id."""
    try:
        db_adaptor = get_db_adaptor()
        return db_adaptor.insert_one(required_fields_digest).inserted_id
    except Exception as e:
        log_exception(e)
        raise errors.InternalServerError()


def insert_users(users_to_insert:
                 List[MutableMapping[Any, Any]]) -> List[str]:
    """Insert new users to collection, return ids."""
    try:
        db_adaptor = get_db_adaptor()
        return db_adaptor.insert_many(users_to_insert).inserted_ids
    except Exception as e:
        log_exception(e)
        raise errors.InternalServerError()


def find_one_by_filter(search_filter: Dict[Union[str, int], Any]) \
        -> Optional[Dict[Union[str, int], Any]]:
    """Find one user by search_filter. Returns user object."""
    try:
        db_adaptor = get_db_adaptor()
        return db_adaptor.find_one(search_filter,
                                   projection={'_id': False})
    except Exception as e:
        log_exception(e)
        raise errors.InternalServerError()


def find_one_by_email(search_filter: Dict[Union[str, int], Any]) \
                      -> Optional[Dict[Union[str, int], Any]]:
    """Find one user by email. Returns user object."""
    try:
        db_adaptor = get_db_adaptor()
        res = db_adaptor.find_one(search_filter,
                                  projection={'_id': False})
        return res if res is not None else None
    except Exception as e:
        log_exception(e)
        raise errors.InternalServerError()


def update_user(user_uuid: str, user_to_db: MutableMapping[Any, Any]) \
                -> Optional[Dict[Union[str, int], Any]]:
    """
    Updates single user object by given user_uuid.
    Raises errors.ResourceNotFound if user is not found by user_uuid.
    Raises errors.InternalServerError is any other errors.
    """
    try:
        fields = {'_id': False}
        db_adaptor = get_db_adaptor()
        return db_adaptor.find_one_and_update(
            {'uuid': user_uuid},
            {'$set': user_to_db},
            projection=fields,
            return_document=ReturnDocument.AFTER
        )
    except errors.UserNotFound as e:
        log_exception(e)
        raise
    except Exception as e:
        log_exception(e)
        raise errors.InternalServerError()
