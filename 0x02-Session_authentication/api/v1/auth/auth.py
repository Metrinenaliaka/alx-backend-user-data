#!/usr/bin/env python3
"""
handling authentication for the API
"""

from typing import TypeVar
import fnmatch
from flask import request, jsonify, abort
from typing import List, TypeVar


class Auth:
    """
    class handling auth
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        required paths"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        # if path in excluded_paths:
        #     return False
        if path[-1] != '/':
            path += '/'
        # if path not in excluded_paths:
        #     return True
        for match in excluded_paths:
            if fnmatch.fnmatch(path, match):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        authorization header
        """
        if request is not None:
            return request.headers.get('Authorization')

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        return None
