from typing import Optional

class App_Rights:
    read: Optional[bool]
    submit: Optional[bool]
    manage: Optional[bool]
    def __init__(self, read, submit, manage) -> None: ...
