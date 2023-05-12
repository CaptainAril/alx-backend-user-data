#!/usr/bin/python3

from bcrypt import hashpw, gensalt, checkpw


def _hash_password(password):
    """ Returns a bcrypt hash of `password`.
    """
    passwd = password.encode('utf-8')
    salt = gensalt()
    return hashpw(passwd, salt)

passwd = input("Enter password: ")
passHash = _hash_password(passwd)
print("encrypted password: {}".format(passHash))
