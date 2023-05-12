#!/usr/bin/env python3
""" auth module.
"""

from bcrypt import hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Returns a bcrypt hash of `password`.
    """
    passwd = password.encode('utf-8')
    salt = gensalt()
    return hashpw(passwd, salt)


class Auth:
    """ Auth class to interact with the authentication databases.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user

        Args:
            email (str): email address of new user
            password (str): password of new user

        Raises:
            ValueError: If user already exists with the passed email.

        Returns:
            User: New User object created.
        """
        try:
            user = self._db.find_user_by(**{'email': email})
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            passwd_hash = _hash_password(password)
            return self._db.add_user(email, passwd_hash)