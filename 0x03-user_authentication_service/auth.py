#!/usr/bin/env python3
""" auth module.
"""

from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """ Returns a bcrypt hash of `password`.
    """
    passwd = password.encode('utf-8')
    salt = gensalt()
    return hashpw(passwd, salt)
