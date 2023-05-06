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
        if not (authorization_header and isinstance(authorization_header, str)
                and authorization_header.startswith('Basic ')):
            return None
        return authorization_header[6:]
