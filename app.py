"""Vercel entrypoint re-exporting the FastAPI application instance.

Allows Vercel zero-configuration deployment to automatically detect
and serve the existing FastAPI application.
"""

import sys
from pathlib import Path

# Resolve project root directory and ensure it is on sys.path for serverless runtimes
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.main import app

__all__ = ["app"]
