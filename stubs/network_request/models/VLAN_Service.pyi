from typing import Literal, Optional

class VLAN_Service:
    name: str
    id: Optional[int]
    description: Optional[str]
    submitter: Optional[str]
    status: Literal["submitted", "approved", "denied"]
    def __post_init__(self) -> None: ...
    def __init__(self, name, id, description, submitter, status) -> None: ...
