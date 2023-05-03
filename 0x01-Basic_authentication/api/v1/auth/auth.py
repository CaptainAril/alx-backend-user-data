#!/usr/bin/env python3
""" Module for Authentication. """

from flask import request
from typing import List, TypeVar


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
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header method.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user method.
        """
        return None
