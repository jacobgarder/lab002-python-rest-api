from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class VLAN_Service:
    """A Basic VLAN Service"""

    name: str
    id: Optional[int] = None
    description: Optional[str] = None
    submitter: Optional[str] = None
    status: Literal["submitted", "approved", "denied"] = "submitted"

    # TODO: Better way to validate or limit values of properties?
    def __post_init__(self):
        """Validate the data for new service"""
        if self.status not in ["submitted", "approved", "denied"]:
            raise ValueError("status must be one of: 'submitted, approved, denied'")
        if self.id is not None and (self.id < 1 or self.id > 4094):
            raise ValueError("id must be between 1..4094")
