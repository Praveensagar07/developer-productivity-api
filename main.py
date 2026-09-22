"""Root entrypoint for Vercel deployment and ASGI application discovery.

Imports and re-exports the existing FastAPI application instance from app.main.
"""

from app.main import app

__all__ = ["app"]
