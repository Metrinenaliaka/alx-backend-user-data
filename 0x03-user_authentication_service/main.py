#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    checks register user response
    """
    url = "http://localhost:5000/register"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    print(response.status_code)
    assert response.status_code == 200
    print("User registered successfully.")


def log_in_wrong_password(email: str, password: str) -> None:
    """
    checks login response with wrong password
    """
    url = "http://localhost:5000/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 401
    print("Login failed with wrong password.")


def log_in(email: str, password: str) -> str:
    """
    checks login response with correct password
    """
    url = "http://localhost:5000/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    print("Logged in successfully.")
    return session_id


def profile_unlogged() -> None:
    """
    checks profile response for unlogged user
    """
    url = "http://localhost:5000/profile"
    response = requests.get(url)
    assert response.status_code == 403
    print("Access to profile denied for unlogged user.")


def profile_logged(session_id: str) -> None:
    """
    checks profile response for logged user
    """
    url = "http://localhost:5000/profile"
    headers = {
        "session_id": session_id
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print("Access to profile granted for logged user.")


def log_out(session_id: str) -> None:
    """
    checks logout response
    """
    url = "http://localhost:5000/logout"
    headers = {
        "session_id": session_id
    }
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200
    print("Logged out successfully.")


def reset_password_token(email: str) -> str:
    """
    checks reset password token response
    """
    url = "http://localhost:5000/reset_password"
    data = {
        "email": email
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    reset_token = response.json()["reset_token"]
    print("Reset password token generated.")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    checks update password response
    """
    url = "http://localhost:5000/update_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, json=data)
    assert response.status_code == 200
    print("Password updated successfully.")


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
