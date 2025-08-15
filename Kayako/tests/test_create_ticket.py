import pytest
from unittest.mock import MagicMock
import requests_mock
from pydantic.v1 import SecretStr
from requests import HTTPError

from kayako_modules import KayakoModule
from kayako_modules.action_create_ticket import KayakoCreateTicket, KayakoCreateTicketArguments

@pytest.fixture
def action():

    action = KayakoCreateTicket(KayakoModule())
    action.log = MagicMock()

    action.module.configuration = {
        "kayako_url": "https://support.doit-solutions.de",
        "kayako_apikey": SecretStr("my-api-key"),
        "kayako_secretkey": SecretStr("my-secret-key")
    }

    return action

def test_create_ticket(action: KayakoCreateTicket):
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "POST",
            "https://support.doit-solutions.de/api/index.php?",
            content=b'<tickets><ticket><tid>3456</tid><contents>new ticket</contents></ticket></tickets>'
        )
        args = KayakoCreateTicketArguments(
            subject="Test Ticket NEU",
            fullname="Max Testermann",
            email="mt@testermann.local",
            contents="This is a long long post",
            departmentid="111",
            ticketstatusid="15",
            ticketpriorityid="3",
            tickettypeid="51",
            userid="1233",
            staffid="111",
            ownerstaffid="111"
        )
        result = action.run(args)
        assert result is not None
        assert result.get("tid") == '3456'
        assert result.get("contents") == "new ticket"

def test_fail_to_create_ticket(action: KayakoCreateTicket):
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "POST",
            "https://support.doit-solutions.de/api/index.php?",
            content=b''
        )
        args = KayakoCreateTicketArguments(
            subject="Some kind of errouneous data",
            fullname="Max Testermann",
            email="mt@testermann.local",
            contents="This is a long long post",
            departmentid="111",
            ticketstatusid="15",
            ticketpriorityid="3",
            tickettypeid="51",
            userid="1233",
            staffid="111",
            ownerstaffid="111"
        )
        result = action.run(args)
        assert result is not None
        assert result == {}

def test_http_error_status(action: KayakoCreateTicket):
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "POST",
            "https://support.doit-solutions.de/api/index.php?",
            status_code=403,
            reason="Invalid Credentials"
        )
        args = KayakoCreateTicketArguments(
            subject="Some kind of errouneous data",
            contents="This is a long long post"
        )
        with pytest.raises(HTTPError):
            result = action.run(args)
            assert result is None