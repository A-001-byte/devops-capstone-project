"""Entry point for gunicorn: `gunicorn wsgi:app`."""
from service import app  # noqa: F401
