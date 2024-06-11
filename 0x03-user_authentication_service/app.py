#!/usr/bin/env python3
"""
my flask app
"""
from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=['DELETE'])
def logout() -> Response:
    """
    logs out users
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        return jsonify({"message": "Forbidden"}), 403


@app.route('/profile', methods=['GET'])
def profile() -> Response:
    """
    gets user profile
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        return jsonify({"message": "Forbidden"}), 403


@app.route('/reset_password', methods=['POST'])
def reset_password() -> Response:
    """
    generates reset password token
    """
    email = request.form.get("email")
    if not email:
        return jsonify({"message": "Email is required"}), 400
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except NoResultFound:
        return jsonify({"message": "Forbidden"}), 403


@app.route('/reset_password', methods=['PUT'])
def update_password() -> Response:
    """
    updates user password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    if not email or not reset_token or not new_password:
        return jsonify({"message": "Email, reset_token,\
                        and new_password are required"}), 400
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        return jsonify({"message": "Invalid reset token"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
