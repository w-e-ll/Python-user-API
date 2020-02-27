# -*- coding: utf-8 -*-

import configparser
import json
import os
import logging

from version import VERSION
from logger_setup import logger

script_dir = os.path.dirname(__file__)
default_config_file = os.path.join(script_dir, "default_config.ini")
logger.debug("Reading from default_config.ini")

config = configparser.ConfigParser()
config.read(default_config_file)

if os.path.exists(os.path.join(script_dir, "config.ini")):
    logger.debug("Reading also from config.ini")
    specific_config_file = os.path.join(script_dir, "config.ini")
    config.read(specific_config_file)


def get_env(section, var, default=None) -> str:
    if "%s_%s" % (section, var) in os.environ:
        return os.environ["%s_%s" % (section, var)]
    elif section in config and var in config[section]:
        return config[section][var]
    else:
        return default


UUID_MATCH_PATTERN = 'USER-[0-9A-F]{32}\\Z'
SUPPORTED_CONTENT_TYPE = 'application/json'
SUPPORTED_METHODS = {
    '/home': {'GET'},
    '/get_user_by_uuid': {'GET'},
    '/get_user_by_email': {'GET'},
    '/count_users': {'GET'},
    '/get_total_users': {'GET'},
    '/post_user': {'POST'},
    '/post_users': {'POST'},
    '/update_user': {'PUT'},
    '/delete_user': {'DELETE'},
    '/drop_collection': {'POST'}
}


def to_boolean(var: str) -> bool:
    return False if str(var).lower() == 'false' \
                 or str(var).lower() == '0' \
                 else True


DATABASE = {
    'ADDRESS': get_env('DATABASE', 'ADDRESS', 'db'),
    'PORT': int(get_env('DATABASE', 'PORT', 27017)),
    'DB_NAME': get_env('DATABASE', 'DB_NAME', 'userAPI'),
    'COL_NAME': get_env('DATABASE', 'COL_NAME', 'users')
}

HTTP_SERVER = {
    'ADDRESS': get_env('HTTP_SERVER', 'ADDRESS'),
}

SERVER_SETTINGS = {
    'SERVER_PORT': int(get_env('SERVER_SETTINGS', 'SERVER_PORT', 8080)),
    'SERVER_IP': get_env('SERVER_SETTINGS', 'SERVER_IP', "0.0.0.0"),
    'WEB_BASE': get_env('SERVER_SETTINGS', 'WEB_BASE', "/api/v1"),
    'WEB_SCHEME': get_env('SERVER_SETTINGS', 'WEB_SCHEME', "http")
}

APPLICATION_SETTINGS = {
    'VERSION': VERSION,
    'BASE_PATH': os.getcwd(),
}

LOG = {
    'LEVEL': get_env('LOG', 'LEVEL', 'INFO')
}

# check sanity and set appropriate logging level
if LOG['LEVEL'] not in logging._levelToName.values():
    LOG['LEVEL'] = 'INFO'
logger.info("Setting LOG_LEVEL to {}.".format(LOG['LEVEL']))
logger.setLevel(LOG['LEVEL'])

logger.debug("APPLICATION_SETTINGS: " + json.dumps(APPLICATION_SETTINGS))
logger.debug("HTTP_SERVER: " + json.dumps(HTTP_SERVER))
logger.debug("DATABASE: " + json.dumps(DATABASE))
logger.debug("SERVER_SETTINGS: " + json.dumps(SERVER_SETTINGS))
logger.debug("LOG: " + json.dumps(LOG))
