#!/usr/bin/env python3
""" Module for Basic Authentication.
"""

from .auth import Auth


class BasicAuth(Auth):
    """ Basic Authentication class
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """ Extracts the base64 authorization value."""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if 'Basic ' not in authorization_header:
            return None
        return authorization_header.removeprefix('Basic ')
