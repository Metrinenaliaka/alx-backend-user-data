#!/usr/bin/env python3
"""
class handles BasicAuth
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from flask import request
import base64


class BasicAuth(Auth):
    """
    handles basic api auth
    """
    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        decodes base64
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        extracts base64
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        extracts user credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        # if ':' not in decoded_base64_authorization_header:
        #     return (None, None)
        split_parts = decoded_base64_authorization_header.split(':', 1)
        if len(split_parts) != 2:
            return (None, None)
        return tuple(split_parts)
        # return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email:
                                     str, user_pwd: str) -> TypeVar('User'):
        """
        returns user object
        """
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        from models.user import User
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if not user or len(user) == 0:
            return None

        user = user[0]
        if user is None or not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns current user
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        extracted = self.extract_base64_authorization_header(auth_header)
        if extracted is None:
            return None
        decoded = self.decode_base64_authorization_header(extracted)
        if decoded is None:
            return None
        user, pwd = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(user, pwd)
