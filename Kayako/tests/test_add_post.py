import pytest
from unittest.mock import MagicMock
import requests_mock
from pydantic.v1 import SecretStr

from kayako_modules import KayakoModule
from kayako_modules.action_add_post import KayakoAddPost, KayakoAddPostArguments

@pytest.fixture
def action():

    action = KayakoAddPost(KayakoModule())
    action.log = MagicMock()

    action.module.configuration = {
        "kayako_url": "https://support.doit-solutions.de",
        "kayako_apikey": SecretStr("my-api-key"),
        "kayako_secretkey": SecretStr("my-secret-key")
    }

    return action

def test_add_post(action: KayakoAddPost):
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "POST",
            "https://support.doit-solutions.de/api/index.php?",
            content=b'<posts><post><id>1234</id><contents>testpost</contents></post></posts>'
        )
        args = KayakoAddPostArguments(
            ticketid="TST-123-456",
            contents="Put your new text here",
            userid=None,
            staffid="100"
        )
        result = action.run(args)
        assert result is not None
        assert result.get("id") == '1234'
        assert result.get("contents") == "testpost"

def test_fail_to_add_post(action: KayakoAddPost):
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "POST",
            "https://support.doit-solutions.de/api/index.php?",
            content=b''
        )
        args = KayakoAddPostArguments(
            ticketid="Invalid Ticket ID",
            contents="Put your new text here",
            userid=None,
            staffid="200"
        )
        result = action.run(args)
        assert result is not None
        assert result == {}