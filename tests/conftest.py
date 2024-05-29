import pytest
from network_request.models.TACACS_Auth import TACACS_Auth
from network_request.models.App_Rights import App_Rights
from network_request import create_app
import logging


@pytest.fixture()
def tacacs():
    tacacs = TACACS_Auth()
    return tacacs


@pytest.fixture()
def operator():
    return {
        "username": "operator",
        "password": "password",
        "rights": App_Rights(read=True, submit=True, manage=False),
    }


@pytest.fixture()
def app():
    app = create_app()
    app.testing = True
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here
    logging.info(f"app.template_folder: {app.template_folder}")

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()
