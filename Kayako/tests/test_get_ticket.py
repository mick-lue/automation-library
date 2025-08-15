import pytest
from unittest.mock import MagicMock
import requests_mock
from pydantic.v1 import SecretStr
from requests import HTTPError

from kayako_modules import KayakoModule
from kayako_modules.action_get_ticket import KayakoGetTicket, KayakoGetTicketArguments

@pytest.fixture
def action():

    action = KayakoGetTicket(KayakoModule())
    action.log = MagicMock()

    action.module.configuration = {
        "kayako_url": "https://support.doit-solutions.de/api/index.php?",
        "kayako_apikey": SecretStr("my-api-key"),
        "kayako_secretkey": SecretStr("my-secret-key"),
        "verify": False
    }

    return action

def test_get_ticket(action: KayakoGetTicket):
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "GET",
            "https://support.doit-solutions.de/api/index.php?",
            content=b'<tickets><ticket><tid>123456789</tid><subject>Already Existing</subject></ticket></tickets>'
        )
        args = KayakoGetTicketArguments(
            ticketid="123456789"
        )
        result = action.run(args)
        assert result is not None
        assert result.get("tid") == '123456789'
        assert result.get("subject") == "Already Existing"

def test_fail_to_get_ticket(action: KayakoGetTicket):
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "GET",
            "https://support.doit-solutions.de/api/index.php?",
            content=b''
        )
        args = KayakoGetTicketArguments(
            ticketid="TST-999-111"
        )
        result = action.run(args)
        assert result is not None
        assert result == {}

def test_http_internal_error_status(action: KayakoGetTicket):
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "GET",
            "https://support.doit-solutions.de/api/index.php?",
            status_code=500,
            reason="Internal Server Error"
        )
        args = KayakoGetTicketArguments(
            ticketid="definitely not an error"
        )
        with pytest.raises(HTTPError):
            result = action.run(args)
            assert result is None