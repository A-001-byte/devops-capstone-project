"""JSON error handlers for the Accounts service."""
from flask import jsonify

from service import app
from service.common import status
from service.models import DataValidationError


def _error(code, name, message):
    return jsonify(status=code, error=name, message=str(message)), code


@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """Turn a validation error into a 400 Bad Request."""
    return _error(status.HTTP_400_BAD_REQUEST, "Bad Request", error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """Handle a 400 Bad Request."""
    return _error(status.HTTP_400_BAD_REQUEST, "Bad Request", error)


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handle a 404 Not Found."""
    return _error(status.HTTP_404_NOT_FOUND, "Not Found", error)


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """Handle a 405 Method Not Allowed."""
    return _error(status.HTTP_405_METHOD_NOT_ALLOWED, "Method not Allowed", error)


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """Handle a 415 Unsupported Media Type."""
    return _error(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Unsupported media type", error)


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """Handle a 500 Internal Server Error."""
    return _error(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error", error)
