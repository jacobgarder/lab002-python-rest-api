import pytest
import logging
from network_request.models.App_Rights import App_Rights


def test_authenticate_01(tacacs, operator):
    logging.info("Testing if authenticating with correct credentials works.")
    authenticate = tacacs.authenticate(operator["username"], operator["password"])
    assert authenticate


def test_authenticate_02(tacacs, operator):
    logging.info("Testing if authenticating with INVALID credentials works.")
    bad_password = "badpass"
    authenticate = tacacs.authenticate(operator["username"], bad_password)
    assert not authenticate


def test_authorize_01(tacacs, operator):
    logging.info("Testing that the returned rights for a user are valid")
    rights = tacacs.authorize(operator["username"])
    assert isinstance(rights, App_Rights)
    assert rights == operator["rights"]


def test_accounting_01(tacacs, operator):
    logging.info("Testing that accounting works.")
    accounting = tacacs.accounting(
        operator["username"], action="Test", message="Testing if accounting works"
    )
    assert accounting
