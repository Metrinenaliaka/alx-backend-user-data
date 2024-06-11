#!/usr/bin/env python3
"""
my flask app
"""
from flask import Flask, jsonify, request, abort
from flask.wrappers import Response
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def message() -> Response:
    """
    simple jsonify response
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> Response:
    """
    registers users
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> Response:
    """
    logs in users
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400
        user = AUTH.valid_login(email, password)
        if not user:
            abort(401)
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    except ValueError as e:
        return jsonify({"message": str(e)}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
