#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Generate a hashed password using the bcrypt algorithm.

    Parameters:
    password (str): The plain text password to be hashed.

    Returns:
    str: The hashed password.

    Raises:
    None

    Note:
    This function uses the CryptContext class from the passlib library to hash the password.
    The hashed password is returned as a string.
    """
    hash: str = pwd_context.hash(password)
    return hash
