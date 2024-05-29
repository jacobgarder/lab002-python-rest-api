from .flags import (
    TAC_PLUS_AUTHEN_LOGIN as TAC_PLUS_AUTHEN_LOGIN,
    TAC_PLUS_AUTHEN_STATUS_ERROR as TAC_PLUS_AUTHEN_STATUS_ERROR,
    TAC_PLUS_AUTHEN_STATUS_FAIL as TAC_PLUS_AUTHEN_STATUS_FAIL,
    TAC_PLUS_AUTHEN_STATUS_GETPASS as TAC_PLUS_AUTHEN_STATUS_GETPASS,
    TAC_PLUS_AUTHEN_STATUS_PASS as TAC_PLUS_AUTHEN_STATUS_PASS,
    TAC_PLUS_AUTHEN_SVC_LOGIN as TAC_PLUS_AUTHEN_SVC_LOGIN,
    TAC_PLUS_PRIV_LVL_MIN as TAC_PLUS_PRIV_LVL_MIN,
    TAC_PLUS_VIRTUAL_PORT as TAC_PLUS_VIRTUAL_PORT,
    TAC_PLUS_VIRTUAL_REM_ADDR as TAC_PLUS_VIRTUAL_REM_ADDR,
)
from _typeshed import Incomplete

class TACACSAuthenticationStart:
    username: Incomplete
    action: Incomplete
    priv_lvl: Incomplete
    authen_type: Incomplete
    service: Incomplete
    data: Incomplete
    rem_addr: Incomplete
    port: Incomplete
    def __init__(
        self, username, authen_type, priv_lvl=..., data=..., rem_addr=..., port=...
    ) -> None: ...
    @property
    def packed(self): ...

class TACACSAuthenticationContinue:
    password: Incomplete
    data: Incomplete
    flags: Incomplete
    def __init__(self, password, data=..., flags: int = ...) -> None: ...
    @property
    def packed(self): ...

class TACACSAuthenticationReply:
    status: Incomplete
    flags: Incomplete
    server_msg: Incomplete
    data: Incomplete
    arguments: Incomplete
    def __init__(self, status, flags, server_msg, data) -> None: ...
    @classmethod
    def unpacked(cls, raw): ...
    @property
    def valid(self): ...
    @property
    def invalid(self): ...
    @property
    def error(self): ...
    @property
    def getpass(self): ...
    @property
    def human_status(self): ...
