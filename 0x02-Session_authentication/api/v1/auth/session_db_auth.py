#!/usr/bin/env python3
"""
session db authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession

class SessionDBAuth(SessionExpAuth):
    """
    session db authentication
    """
    def create_session(self, user_id=None):
        """
        creates a session
        """
        session_id = super().create_session(user_id)
        UserSession(user_id=user_id, session_id=session_id).save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns a User ID based on a Session ID
        """
        user_session = UserSession.get(session_id=session_id)
        if user_session:
            return user_session.user_id

    def destroy_session(self, request=None):
        session_id = self.session_cookie(request)
        if session_id:
            user_session = UserSession.get(session_id=session_id)
            if user_session:
                user_session.remove()
                return True
        return False
