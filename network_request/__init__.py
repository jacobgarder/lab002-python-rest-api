from flask import Flask

# from .auth import bp as auth_bp
from network_request import auth, home, services
from network_request import apis

import os
import logging

logging_level = os.getenv("APP_LOGGING_LEVEL", "info")

log_format = "[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(filename)s] [%(funcName)s():%(lineno)s] %(message)s"
log_datefmt = "%d/%m/%Y %H:%M:%S"

if logging_level == "debug":
    log_level = logging.DEBUG
else:
    log_level = logging.INFO

logging.basicConfig(level=log_level, format=log_format, datefmt=log_datefmt)

# Check ot see if sample data env is set
if os.getenv("LOAD_SAMPLE_DATA"):
    import network_request.sample_data  # noqa F401


def create_app(configfile=None):
    # We are using the "Application Factory"-pattern here, which is described
    # in detail inside the Flask docs:
    # http://flask.pocoo.org/docs/patterns/appfactories/

    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(services.bp)
    app.register_blueprint(apis.bp, url_prefix="/api/v1")
    # TODO: Register the blueprint from the apis.py module to leverage a URL prefix of "/api/v1"

    # Create a secret key for session encoding
    app.secret_key = b"SuperSecretKey"

    return app
