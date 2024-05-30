#!/usr/bin/env python3
"""
encypting passwords
"""
import bcrypt
from typing import bytes


def hash_password(password: str) -> bytes:
    """
    a function that hashes a password
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password
