#!/usr/bin/env python3
""" Basic Flask app.
"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def get():
    """Basic flask route.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """ End point to register a user.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": "{}".format(email),
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registerd"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Login function that creates a session, logs in user by session id,
    and returns session id as cookie.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        return abort(401)
    sess_id = AUTH.create_session(email)
    res = jsonify({"email": "{}".format(email), "message": "logged in"})
    res.set_cookie("session_id", sess_id)
    return res


@app.route('/sessions', methods=["DELETE"])
def logout():
    """ User logout endpoint.
    """
    sess_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(sess_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('login'))
    return abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """ User profile endpoint.
    """
    sess_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(sess_id)
    if user:
        return jsonify({"email": "{}".format(user.email)}), 200
    return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
