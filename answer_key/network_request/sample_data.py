from network_request.services import service_list
from .models.VLAN_Service import VLAN_Service
from uuid import uuid4

service_list[uuid4().int] = VLAN_Service(
    id=701, name="Dev01", description="Dev Service 01", submitter="devdata"
)

service_list[uuid4().int] = VLAN_Service(
    id=702, name="Dev02", description="Dev Service 02", submitter="devdata"
)

service_list[uuid4().int] = VLAN_Service(
    id=703,
    name="Dev03",
    description="Dev Service 03",
    submitter="devdata",
    status="approved",
)
service_list[uuid4().int] = VLAN_Service(
    id=704,
    name="Dev04",
    description="Dev Service 04",
    submitter="devdata",
    status="approved",
)
service_list[uuid4().int] = VLAN_Service(
    id=705,
    name="Dev05",
    description="Dev Service 05",
    submitter="devdata",
    status="denied",
)
