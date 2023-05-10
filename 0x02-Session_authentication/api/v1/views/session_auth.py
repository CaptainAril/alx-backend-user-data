#!/usr/bin/env python3
""" View module for Session authentication.
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handles session creation at user login.

    Returns:
        User: returns user and set session id cookie
            if user found based on email in request.
        Error: If no user found.
    """
    email = request.form.get('email')
    passwd = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not passwd:
        return jsonify({"error": "password missing"}), 400

    user_list = User.search({'email': email})

    if len(user_list) > 0:
        user = user_list[0]
        if not user.is_valid_password(passwd):
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        sess_id = auth.create_session(user.id)

        res = jsonify(user.to_json())
        _sess_id = getenv('SESSION_NAME')
        res.set_cookie(_sess_id, sess_id)
        return res
    return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ Logs out user and destroy's session.
    """
    from api.v1.app import auth
    sess = auth.destroy_session(request)
    if sess:
        return jsonify({}), 200
    else:
        return abort(404)
