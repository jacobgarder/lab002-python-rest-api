from dataclasses import dataclass
from typing import Optional


@dataclass
class App_Rights:
    read: Optional[bool] = False
    submit: Optional[bool] = False
    manage: Optional[bool] = False
