from .flags import (
    TAC_PLUS_AUTHEN_SVC_LOGIN as TAC_PLUS_AUTHEN_SVC_LOGIN,
    TAC_PLUS_AUTHOR_STATUS_ERROR as TAC_PLUS_AUTHOR_STATUS_ERROR,
    TAC_PLUS_AUTHOR_STATUS_FAIL as TAC_PLUS_AUTHOR_STATUS_FAIL,
    TAC_PLUS_AUTHOR_STATUS_FOLLOW as TAC_PLUS_AUTHOR_STATUS_FOLLOW,
    TAC_PLUS_AUTHOR_STATUS_PASS_ADD as TAC_PLUS_AUTHOR_STATUS_PASS_ADD,
    TAC_PLUS_AUTHOR_STATUS_PASS_REPL as TAC_PLUS_AUTHOR_STATUS_PASS_REPL,
    TAC_PLUS_VIRTUAL_PORT as TAC_PLUS_VIRTUAL_PORT,
    TAC_PLUS_VIRTUAL_REM_ADDR as TAC_PLUS_VIRTUAL_REM_ADDR,
)
from _typeshed import Incomplete

class TACACSAuthorizationStart:
    username: Incomplete
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
        authen_method,
        priv_lvl,
        authen_type,
        arguments,
        rem_addr=...,
        port=...,
    ) -> None: ...
    @property
    def packed(self): ...

class TACACSAuthorizationReply:
    status: Incomplete
    arg_cnt: Incomplete
    server_msg: Incomplete
    data: Incomplete
    arguments: Incomplete
    flags: Incomplete
    def __init__(self, status, arg_cnt, server_msg, data, arguments) -> None: ...
    @classmethod
    def unpacked(cls, raw): ...
    @property
    def valid(self): ...
    @property
    def invalid(self): ...
    @property
    def error(self): ...
    @property
    def reply(self): ...
    @property
    def follow(self): ...
    @property
    def human_status(self): ...
