#!/usr/bin/env python3
"""
authentication module
"""
import uuid
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    takes a password and hashes it
    """
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    hash_password = bcrypt.hashpw(password_bytes, salt)
    return hash_password


def _generate_uuid() -> str:
    """
    generates a uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        constructor
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registers a user to a database
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hash_pass = _hash_password(password)
        new_user = self._db.add_user(email, hash_pass)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        checks validity of a user
        """
        try:
            user = self._db.find_user_by(email=email)
            stored_hashed_password = user.hashed_password
            password_bytes = password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, stored_hashed_password)
        except NoResultFound as exc:
            raise ValueError from exc

    def create_session(self, email: str) -> str:
        """
        creates a session
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, email=email, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        gets a user from a session id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroys a session
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        generates a reset token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound as exc:
            raise ValueError from exc

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, token: str, password: str) -> None:
        """
        updates a password
        """
        try:
            user = self._db.find_user_by(reset_token=token)
        except NoResultFound:
            raise ValueError

        hash_pass = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hash_pass)
        self._db.update_user(user.id, reset_token=None)
