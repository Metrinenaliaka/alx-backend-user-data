#!/usr/bin/env python3
"""
handling authentication for the API
"""
import os
from typing import TypeVar
import uuid
from api.v1.auth.auth import Auth

os.environ['AUTH_TYPE'] = 'SessionAuth'
def get_auth_class():
    """
    returns the authentication class
    """
    auth_type = os.getenv('AUTH_TYPE', 'Auth')
    if auth_type == 'SessionAuth':
        return SessionAuth
    else:
        return Auth

# Validate the switch
def validate_switch():
    AuthClass = get_auth_class()
    auth_instance = AuthClass()
    auth_instance.authenticate()


class SessionAuth(Auth):
    """
    class for session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns a User instance based on a cookie value
        """
        from models.user import User
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        destroys a session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
