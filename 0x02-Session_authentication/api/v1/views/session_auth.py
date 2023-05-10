#!/usr/bin/env python3
""" View module to handle all routes
for the Session authentication.
"""

from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def post_view():
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
    return jsonify({"error": "no user found for this email"}), 401
