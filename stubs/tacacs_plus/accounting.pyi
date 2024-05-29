from .flags import (
    TAC_PLUS_ACCT_STATUS_ERROR as TAC_PLUS_ACCT_STATUS_ERROR,
    TAC_PLUS_ACCT_STATUS_FOLLOW as TAC_PLUS_ACCT_STATUS_FOLLOW,
    TAC_PLUS_ACCT_STATUS_SUCCESS as TAC_PLUS_ACCT_STATUS_SUCCESS,
    TAC_PLUS_AUTHEN_SVC_LOGIN as TAC_PLUS_AUTHEN_SVC_LOGIN,
    TAC_PLUS_VIRTUAL_PORT as TAC_PLUS_VIRTUAL_PORT,
    TAC_PLUS_VIRTUAL_REM_ADDR as TAC_PLUS_VIRTUAL_REM_ADDR,
)
from _typeshed import Incomplete

class TACACSAccountingStart:
    username: Incomplete
    flags: Incomplete
    authen_method: Incomplete
    priv_lvl: Incomplete
    authen_type: Incomplete
    service: Incomplete
    arguments: Incomplete
    rem_addr: Incomplete
    port: Incomplete
    def __init__(
        self,
        username,
        flags,
        authen_method,
        priv_lvl,
        authen_type,
        arguments,
        rem_addr=...,
        port=...,
    ) -> None: ...
    @property
    def packed(self): ...

class TACACSAccountingReply:
    status: Incomplete
    server_msg: Incomplete
    data: Incomplete
    flags: Incomplete
    arguments: Incomplete
    def __init__(self, status, server_msg, data) -> None: ...
    @classmethod
    def unpacked(cls, raw): ...
    @property
    def valid(self): ...
    @property
    def error(self): ...
    @property
    def follow(self): ...
    @property
    def human_status(self): ...
