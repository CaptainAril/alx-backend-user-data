#!/usr/bin/env python3
""" Module for Basic Authentication.
"""

from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentication class
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """ Extracts the base64 authorization value."""
        if not (authorization_header and isinstance(authorization_header, str)
                and authorization_header.startswith('Basic ')):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ Returns the decoded value of a Base64 string.
        """
        if not (base64_authorization_header
                and isinstance(base64_authorization_header, str)):
            return None
        try:
            decoded_value = base64.b64decode(base64_authorization_header)
            return decoded_value.decode('UTF-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorizaton_header: str) -> (str, str):
        """ Returns the user email and password
        from the Base64 decoded value."""
        if not (decoded_base64_authorizaton_header and
                isinstance(decoded_base64_authorizaton_header, str) and
                ':' in decoded_base64_authorizaton_header):
            return None, None
        name, passwd = decoded_base64_authorizaton_header.split(':')
        return name, passwd

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ Returns the `User` instance based on email and passeord.
        """
        usr = User()
        if not (user_email or isinstance(user_email, str)):
            return None
        if not (user_pwd or isinstance(user_pwd, str)):
            return None
        user_list = usr.search({'email': user_email})
        if len(user_list) > 0:
            user = user_list[0]
            return user if user.is_valid_password(user_pwd) else None
