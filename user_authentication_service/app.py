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
    password = request.form.get('password'