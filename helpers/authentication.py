import requests

import confighelper

config = confighelper.instance()

__AUTHENTICATION_URI = config.auth_uri
BOXSET_AUTHENTICATION_URI = config.boxset_auth_uri
TEST_USER_NAME, __PASSWORD = config.login_details


def get_auth_token(user_name=None, password=None):
    if not (user_name and password):
        user_name = TEST_USER_NAME
        password = __PASSWORD
    res = requests.get(__AUTHENTICATION_URI, None, headers={'UserId': user_name, 'Password': password})
    return res.content


def get_boxset_auth_token(user_name=None, password=None):
    if not (user_name and password):
        user_name = TEST_USER_NAME
        password = __PASSWORD
    res = requests.get(BOXSET_AUTHENTICATION_URI, None, headers={'UserId': user_name, 'Password': password})
    return res.content
