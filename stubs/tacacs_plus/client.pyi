from .accounting import (
    TACACSAccountingReply as TACACSAccountingReply,
    TACACSAccountingStart as TACACSAccountingStart,
)
from .authentication import (
    TACACSAuthenticationContinue as TACACSAuthenticationContinue,
    TACACSAuthenticationReply as TACACSAuthenticationReply,
    TACACSAuthenticationStart as TACACSAuthenticationStart,
)
from .authorization import (
    TACACSAuthorizationReply as TACACSAuthorizationReply,
    TACACSAuthorizationStart as TACACSAuthorizationStart,
)
from .flags import (
    TAC_PLUS_ACCT as TAC_PLUS_ACCT,
    TAC_PLUS_AUTHEN as TAC_PLUS_AUTHEN,
    TAC_PLUS_AUTHEN_METH_TACACSPLUS as TAC_PLUS_AUTHEN_METH_TACACSPLUS,
    TAC_PLUS_AUTHEN_STATUS_FAIL as TAC_PLUS_AUTHEN_STATUS_FAIL,
    TAC_PLUS_AUTHEN_TYPE_ASCII as TAC_PLUS_AUTHEN_TYPE_ASCII,
    TAC_PLUS_AUTHEN_TYPE_CHAP as TAC_PLUS_AUTHEN_TYPE_CHAP,
    TAC_PLUS_AUTHEN_TYPE_PAP as TAC_PLUS_AUTHEN_TYPE_PAP,
    TAC_PLUS_AUTHOR as TAC_PLUS_AUTHOR,
    TAC_PLUS_AUTHOR_STATUS_FAIL as TAC_PLUS_AUTHOR_STATUS_FAIL,
    TAC_PLUS_CONTINUE_FLAG_ABORT as TAC_PLUS_CONTINUE_FLAG_ABORT,
    TAC_PLUS_MAJOR_VER as TAC_PLUS_MAJOR_VER,
    TAC_PLUS_MINOR_VER as TAC_PLUS_MINOR_VER,
    TAC_PLUS_MINOR_VER_ONE as TAC_PLUS_MINOR_VER_ONE,
    TAC_PLUS_PRIV_LVL_MAX as TAC_PLUS_PRIV_LVL_MAX,
    TAC_PLUS_PRIV_LVL_MIN as TAC_PLUS_PRIV_LVL_MIN,
    TAC_PLUS_VIRTUAL_PORT as TAC_PLUS_VIRTUAL_PORT,
    TAC_PLUS_VIRTUAL_REM_ADDR as TAC_PLUS_VIRTUAL_REM_ADDR,
)
from .packet import TACACSHeader as TACACSHeader, TACACSPacket as TACACSPacket
from _typeshed import Incomplete
from collections.abc import Generator

logger: Incomplete

class TACACSClient:
    host: Incomplete
    port: Incomplete
    secret: Incomplete
    timeout: Incomplete
    version_max: Incomplete
    version_min: Incomplete
    family: Incomplete
    session_id: Incomplete
    def __init__(
        self,
        host,
        port,
        secret,
        timeout: int = ...,
        session_id: Incomplete | None = ...,
        family=...,
        version_max=...,
        version_min=...,
    ) -> None: ...
    @property
    def version(self): ...
    @property
    def sock(self): ...
    def closing(self) -> Generator[None, None, None]: ...
    def send(self, body, req_type, seq_no: int = ...): ...
    def authenticate(
        self,
        username,
        password,
        priv_lvl=...,
        authen_type=...,
        chap_ppp_id: Incomplete | None = ...,
        chap_challenge: Incomplete | None = ...,
        rem_addr=...,
        port=...,
    ): ...
    def authorize(
        self,
        username,
        arguments=...,
        authen_type=...,
        priv_lvl=...,
        rem_addr=...,
        port=...,
    ): ...
    def account(
        self,
        username,
        flags,
        arguments=...,
        authen_type=...,
        priv_lvl=...,
        rem_addr=...,
        port=...,
    ): ...
