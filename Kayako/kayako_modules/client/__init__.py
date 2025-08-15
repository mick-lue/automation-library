import requests
import random
import hmac
import hashlib
import base64
import urllib3
from requests_ratelimiter import LimiterAdapter


class ApiClient(requests.Session):
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        verify: bool,
        max_retries: int = 5,
        ratelimit_per_second: int = 10,
    ):
        super().__init__()
        salt: str = str(random.getrandbits(32))
        signature = base64.encodebytes(hmac.new(key=secret_key.encode(), msg=salt.encode(), digestmod=hashlib.sha256).digest())
        self.mount(
            "https://",
            LimiterAdapter(
                per_second=ratelimit_per_second,
                max_retries=max_retries,
            ),
        )
        self.verify = verify
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.params = {"apikey": api_key, "salt": salt, "signature": signature}
