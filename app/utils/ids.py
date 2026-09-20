"""Identifier generation utilities."""

import uuid


def generate_id(prefix: str | None = None) -> str:
    """Generate a clean, unique identifier with an optional entity prefix.
    
    Examples:
        generate_id("usr") -> "usr_3f4a8b2c1d0e"
        generate_id()      -> "3f4a8b2c1d0e4f5a9b8c7d6e5f4a3b2c"
    """
    raw_id = uuid.uuid4().hex
    if prefix:
        return f"{prefix}_{raw_id[:16]}"
    return raw_id
