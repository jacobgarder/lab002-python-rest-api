from _typeshed import Incomplete

def crypt(header, body_bytes, secret): ...

class TACACSPacket:
    header: Incomplete
    body_bytes: Incomplete
    secret: Incomplete
    def __init__(self, header, body_bytes, secret) -> None: ...
    @property
    def encrypted(self): ...
    @property
    def seq_no(self): ...
    @property
    def body(self): ...
    def __bytes__(self): ...
    @property
    def crypt(self): ...

class TACACSHeader:
    version: Incomplete
    type: Incomplete
    session_id: Incomplete
    length: Incomplete
    seq_no: Incomplete
    flags: Incomplete
    def __init__(
        self, version, type, session_id, length, seq_no: int = ..., flags: int = ...
    ) -> None: ...
    @property
    def version_max(self): ...
    @property
    def version_min(self): ...
    @property
    def packed(self): ...
    @classmethod
    def unpacked(cls, raw): ...
