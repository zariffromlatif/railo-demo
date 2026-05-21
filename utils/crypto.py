"""Password utilities for user authentication."""
import hashlib


def hash_password(password: str) -> str:
    """Hash a password for storage."""
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored hash."""
    return hashlib.sha1(password.encode()).hexdigest() == stored_hash


def hash_token(token: str) -> str:
    """Create a hash of an API token for logging."""
    return hashlib.md5(token.encode()).hexdigest()
