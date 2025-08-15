from abc import abstractmethod
from functools import cached_property
from typing import Any, OrderedDict
import xmltodict

import requests
from urllib3.util import parse_url, Url
from sekoia_automation.action import Action

from . import KayakoModule
from .client import ApiClient


class KayakoAction(Action):
    module: KayakoModule

    @cached_property
    def client(self) -> ApiClient:
        return ApiClient(api_key=self.module.configuration.kayako_apikey.get_secret_value(), secret_key=self.module.configuration.kayako_secretkey.get_secret_value(), verify=not self.module.configuration.trust_any_cert)

    @cached_property
    def base_url(self) -> str:
        if self.module.configuration.kayako_url.endswith("/api/index.php?"):
            return self.module.configuration.kayako_url
        url: Url = parse_url(self.module.configuration.kayako_url)
        return (str(url.scheme) + "://" if url.scheme in ("http", "https") else "") + (url.authority if url.authority else "") + "/api/index.php?"

    def get_json(self, **kwargs) -> OrderedDict[str, Any] | None:
        response = self.client.get(self.base_url, timeout=60, **kwargs)
        self._handle_response_error(response)
        return xmltodict.parse(response.content) if len(response.content) > 0 else None

    def post_json(self, **kwargs) -> OrderedDict[str, Any] | None:
        response = self.client.post(self.base_url, timeout=60, **kwargs)
        self._handle_response_error(response)
        return xmltodict.parse(response.content) if len(response.content) > 0 else None

    def _handle_response_error(self, response: requests.Response):
        if not response.ok:
            message = f"Request to Kayako API failed with status {response.status_code} - {response.reason}"
            if response.status_code >= 400:
                try:
                    data = response.json()
                    detailed_errors = data.get("errorMessages", [response.text])
                    message = f"{message}: \n {','.join(detailed_errors)}"
                except requests.exceptions.JSONDecodeError:
                    message = f"{message}: \nNo data in response."

            self.log(message=message, level="error")
            response.raise_for_status()

    @abstractmethod
    def run(self, arguments: Any) -> Any:
        raise NotImplementedError