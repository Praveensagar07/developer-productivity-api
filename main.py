"""Root entrypoint for Vercel deployment and ASGI application discovery.

Imports and re-exports the existing FastAPI application instance from app.main.
Ensures repository root is present in sys.path for serverless runtimes.
"""

import sys
from pathlib import Path

# Resolve project root directory from this file and ensure it is on sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.main import app

__all__ = ["app"]

