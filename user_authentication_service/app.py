#!/usr/bin/env python3
"""Route module for basic Flask app API"""

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """GET /
    Returns welcome message
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """POST /users
    JSON: email, password
    Register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 201
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """POST /sessions
    JSON: email, password
    Login user
    """
    user_email = request.form.get('email', '')
    user_password = request.form.get('password', '')
    if not AUTH.valid_login(user_email, user_password):
        abort(401)
    response = make_response(jsonify({"email": user_email, "message": "logged in"}))
    response.set_cookie('session_id', AUTH.create_session(user_email))
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """DELETE /sessions
    Logout user, destroy session
    Return JSON message 'OK' to satisfy tests
    """
    user_cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return jsonify({"message": "OK"}), 200


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """GET /profile
    Return user email if session is valid
    """
    user_cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token_route():
    """POST /reset_password
    JSON: email
    Generate reset token if email registered
    """
    user_email = request.form.get('email', '')
    user = AUTH.get_user_by_email(user_email)
    if user is None:
        abort(403)
    token = AUTH.get_reset_password_token(user_email)
    return jsonify({"email": user_email, "reset_token": token}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """PUT /reset_password
    JSON: email, reset_token, new_password
    Update user password
    """
    user_email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)
    return jsonify({"email": user_email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)