#!/usr/bin/env python3

import requests
import json

url = 'http://127.0.0.1:5000/'


def register_user(email: str, password: str) -> None:
    """User registered.
    """
    data = {'email': email, 'password': password}
    re = requests.post(url+'/users', data=data)
    b = b'{"email":"guillaume@holberton.io","message":"user created"}\n'
    assert re.content == b
    assert re.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Wrong login credentials.
    """
    data = {"email": email, "password": password}
    re = requests.post(url+'sessions', data=data)
    assert re.status_code == 401


def log_in(email: str, password: str) -> str:
    """User login successful.
    """
    data = {"email": email, "password": password}
    re = requests.post(url+'sessions', data=data)
    message = b'{"email":"guillaume@holberton.io","message":"logged in"}\n'
    assert re.content == message
    assert re.status_code == 200
    sess_id = re.cookies.get('session_id')
    return sess_id


def profile_unlogged() -> None:
    """"User not logged in.
    """
    re = requests.get(url+'/profile')
    assert re.status_code == 403


def profile_logged(session_id: str) -> None:
    """Logged in User profile.
    """
    cookie = {"session_id": session_id}
    re = requests.get(url+'/profile', cookies=cookie)
    message = b'{"email":"guillaume@holberton.io"}\n'
    assert re.content == message
    assert re.status_code == 200


def log_out(session_id: str) -> None:
    """"User logout.
    """
    cookie = {"session_id": session_id}
    re = requests.delete(url+'/sessions', cookies=cookie)
    assert re.status_code == 405


def reset_password_token(email: str) -> str:
    """"Password reset token.
    """
    data = {"email": email}
    re = requests.post(url+'/reset_password', data=data)
    assert re.status_code == 200
    token = json.loads(re.content).get('reset_token')
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Reset password.
    """
    data = {"email": email,
            "reset_token": reset_token,
            "new_password": new_password}
    re = requests.put(url+'/reset_password', data=data)
    message = ('{"email":"guillaume@holberton.io",'
               '"message":"Password updated"}\n')
    message = message.encode('utf-8')
    assert re.content == message
    assert re.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
