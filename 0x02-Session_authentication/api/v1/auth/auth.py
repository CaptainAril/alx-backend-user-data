#!/usr/bin/env python3
""" Module for Authentication. """

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Class to manage the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ public method
        """
        if not path:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or path+'/' in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                pt = excluded_path[:-1]
                if path.startswith(pt):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header method.
        """
        if not request:
            return None
        value = request.headers.get('Authorization')
        return value

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user method.
        """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request.
        """
        if not request:
            return None
        _my_session_id = getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
