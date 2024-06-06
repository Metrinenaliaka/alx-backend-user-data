#!/usr/bin/env python3
"""
handling authentication for the API
"""
import os
from api.v1.auth.auth import Auth

os.environ['AUTH_TYPE'] = 'SessionAuth'

class SessionAuth(Auth):
    """
    class for session authentication
    """
    pass
