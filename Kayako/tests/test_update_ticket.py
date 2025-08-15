import pytest
from unittest.mock import MagicMock
import requests_mock
from pydantic.v1 import SecretStr
from requests import HTTPError

from kayako_modules import KayakoModule
from kayako_modules.action_update_ticket import KayakoUpdateTicket, KayakoUpdateTicketArguments

@pytest.fixture
def action():

    action = KayakoUpdateTicket(KayakoModule())
    action.log = MagicMock()

    action.module.configuration = {
        "kayako_url": "https://support.doit-solutions.de",
        "kayako_apikey": SecretStr("my-api-key"),
        "kayako_secretkey": SecretStr("my-secret-key")
    }

    return action

def test_update_ticket(action: KayakoUpdateTicket):
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "POST",
            "https://support.doit-solutions.de/api/index.php?",
            content=b'<tickets><ticket><tid>987654</tid><subject>New Test Subject</subject></ticket></tickets>'
        )
        args = KayakoUpdateTicketArguments(
            ticketid="123456789",
            subject="Test Ticket NEU",
            fullname="Max Testermann",
            email="mt@testermann.local",
            departmentid="111",
            ticketstatusid="15",
            ticketpriorityid="3",
            tickettypeid="51",
            ownerstaffid="111"
        )
        result = action.run(args)
        assert result is not None
        assert result.get("tid") == '987654'
        assert result.get("subject") == "New Test Subject"

def test_fail_to_update_ticket(action: KayakoUpdateTicket):
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "POST",
            "https://support.doit-solutions.de/api/index.php?",
            content=b''
        )
        args = KayakoUpdateTicketArguments(
            ticketid="TST-999-111",
            subject="Not changeable",
            fullname="Max Testermann",
            email="mt@testermann.local"
        )
        result = action.run(args)
        assert result is not None
        assert result == {}

def test_http_internal_error_status(action: KayakoUpdateTicket):
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "POST",
            "https://support.doit-solutions.de/api/index.php?",
            status_code=500,
            reason="Internal Server Error"
        )
        args = KayakoUpdateTicketArguments(
            ticketid="definitely not an error",
            subject="Some kind of errouneous data"
        )
        with pytest.raises(HTTPError):
            result = action.run(args)
            assert result is None