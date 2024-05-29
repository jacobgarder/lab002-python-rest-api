import pytest
import logging
from network_request.models.VLAN_Service import VLAN_Service


def test_basic_vlan():
    logging.info("Testing the creation of a basic, valid VLAN")
    # Test 1
    vlan = VLAN_Service(
        id=11,
        name="test-vlan-01",
        description="pytest good vlan",
        submitter="pytest",
        status="submitted",
    )
    assert isinstance(vlan, VLAN_Service)

    # Test 2
    vlan = VLAN_Service(
        id=12,
        name="test-vlan-02",
        description="pytest good vlan",
        submitter="pytest",
        status="approved",
    )
    assert isinstance(vlan, VLAN_Service)

    # Test 3
    vlan = VLAN_Service(
        id=13,
        name="test-vlan-03",
        description="pytest good vlan",
        submitter="pytest",
        status="denied",
    )
    assert isinstance(vlan, VLAN_Service)


def test_invalid_vlan_id():
    logging.info("Testing that an invalid id will raise ValueError")

    bad_vlans = [{"id": 5000, "name": "vl5000"}, {"id": 0, "name": "vl0"}]
    for bad_vlan in bad_vlans:
        logging.info(
            f"Testing that an invalid id [{bad_vlan['id']}] will raise ValueError"
        )
        with pytest.raises(ValueError):
            vlan = VLAN_Service(
                id=bad_vlan["id"],
                name=bad_vlan["name"],
            )
            if vlan:
                logging.error(f"A VLAN_Service instance was created: {vlan}")


def test_invalid_vlan_status():
    logging.info("Testing that an invalid status ValueError")
    # Test to large
    with pytest.raises(ValueError):
        vlan = VLAN_Service(id=101, name="test-vlan", status="BAD")
