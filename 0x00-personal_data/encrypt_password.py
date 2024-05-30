#!/usr/bin/env python3
"""
encypting passwords
"""
import bcrypt
# from typing import bytes


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    a function that checks if a password is valid
    """
    # Check if the provided password matches the hashed password
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    else:
        return False


def hash_password(password: str) -> bytes:
    """
    a function that hashes a password
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password
