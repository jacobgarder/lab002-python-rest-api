from .App_Rights import App_Rights as App_Rights
from tacacs_plus.client import TACACSClient
from tacacs_plus.flags import (
    TAC_PLUS_ACCT_FLAG_STOP as TAC_PLUS_ACCT_FLAG_STOP,
    TAC_PLUS_ACCT_FLAG_WATCHDOG as TAC_PLUS_ACCT_FLAG_WATCHDOG,
)
from typing import Optional

class TACACS_Auth:
    server: Optional[str]
    secret_key: Optional[str]
    tacacs_port: Optional[int]
    application_name: Optional[str]
    aaa_port: Optional[str]
    client: Optional[TACACSClient]
    @staticmethod
    def authorization_args_to_dict(arguments: list) -> dict[str, str]: ...
    def authenticate(self, username: str, password: str) -> bool: ...
    def authorize(self, username: str) -> App_Rights: ...
    def accounting(self, username: str, action: str, message: str) -> bool: ...
    def __init__(
        self, server, secret_key, tacacs_port, application_name, aaa_port, client
    ) -> None: ...
