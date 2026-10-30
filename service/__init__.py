"""Accounts service: Flask app with Talisman security headers and CORS."""
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

# Create the Flask app and load its configuration
app = Flask(__name__)
app.config.from_object("service.config")

# Security headers (HTTPS redirect, X-Frame-Options, CSP, ...) and CORS policy
talisman = Talisman(app)
CORS(app)

# The imports below need `app`, so they come after it is created
# pylint: disable=wrong-import-position,cyclic-import
from service import models, routes  # noqa: E402,F401
from service.common import error_handlers  # noqa: E402,F401

models.Account.init_db(app)
