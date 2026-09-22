"""Vercel Serverless Function entrypoint.

Imports and exposes the existing FastAPI application instance from app.main.
"""

import sys
from pathlib import Path

# Ensure repository root is on sys.path so 'app' package is discoverable
_ROOT_DIR = Path(__file__).resolve().parent.parent
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

from app.main import app

__all__ = ["app"]
