import base64
import json

# Credentials for Auth
valid_operator = base64.b64encode(b"operator:password").decode("utf-8")
valid_customer = base64.b64encode(b"customer:password").decode("utf-8")
valid_sysadmin = base64.b64encode(b"sysadmin:password").decode("utf-8")
invalid_operator = base64.b64encode(b"operator:badpassword").decode("utf-8")
invalid_customer = base64.b64encode(b"customer:badpassword").decode("utf-8")
invalid_sysadmin = base64.b64encode(b"sysadmin:badpassword").decode("utf-8")

# Payloads for test
valid_post = {"name": "pytest_01", "description": "New Test Service "}
invalid_post = {"service_name": "pytest_01", "description": "New Test Service "}
valid_put = {
    "name": "pytest_02",
    "description": "Updated with by pyTest",
    "submitter": "pytester",
    "id": "101",
    "status": "denied",
}
invalid_put = {
    "name": "pytest_02",
    "description": "Updated with by pyTest",
    "submitter": "pytester",
    "id": "101",
    "status": "denied",
    "bad_key": "badbadbad",
}
valid_patch = {
    "status": "approved",
}
invalid_patch_status = {
    "status": "yes",
}

# Status Options For Testing
valid_status = ["approved", "denied", "submitted"]
invalid_status = [
    "yes",
    "no",
    True,
    False,
    "OK",
    "Good",
    "Bad",
]

# Authentication Required Tests
def test_get_services_auth_required(client):
    response = client.get("/api/v1/services")
    assert response.status_code == 401


def test_post_services_auth_required(client):
    response = client.post("/api/v1/services")
    assert response.status_code == 401


def test_put_services_auth_required(client):
    response = client.put("/api/v1/services/0001010101")
    assert response.status_code == 401


def test_patch_services_auth_required(client):
    response = client.patch("/api/v1/services/0001010101")
    assert response.status_code == 401


def test_delete_services_auth_required(client):
    response = client.delete("/api/v1/services/0001010101")
    assert response.status_code == 401


# Basic tests of API functionality
#  The following tests are for proper working API calls
def test_get_services_works(client):
    response = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_operator}"}
    )
    assert response.status_code == 200


def test_post_services_works(client):
    response = client.post(
        "/api/v1/services",
        headers={
            "Authorization": f"Basic {valid_customer}",
            "Content-Type": "application/json",
        },
        data=json.dumps(valid_post),
    )
    assert response.status_code == 201


def test_put_services_works(client):
    lookup = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_operator}"}
    )
    results = json.loads(lookup.data)
    uuid = list(results.keys())[0]

    response = client.put(
        f"/api/v1/services/{uuid}",
        headers={
            "Authorization": f"Basic {valid_sysadmin}",
            "Content-Type": "application/json",
        },
        data=json.dumps(valid_put),
    )
    assert response.status_code == 204


def test_patch_services_works(client):
    lookup = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_operator}"}
    )
    results = json.loads(lookup.data)
    uuid = list(results.keys())[0]

    response = client.patch(
        f"/api/v1/services/{uuid}",
        headers={
            "Authorization": f"Basic {valid_sysadmin}",
            "Content-Type": "application/json",
        },
        data=json.dumps(valid_patch),
    )
    assert response.status_code == 204


def test_delete_services_works(client):
    lookup = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_operator}"}
    )
    results = json.loads(lookup.data)
    uuid = list(results.keys())[0]

    response = client.delete(
        f"/api/v1/services/{uuid}",
        headers={
            "Authorization": f"Basic {valid_sysadmin}",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 204


# Verify proper rights required for API calls
#  The following tests are for proper working API calls
def test_get_services_unauthorized(client):
    response = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_customer}"}
    )
    assert response.status_code == 403


def test_put_services_unauthorized(client):
    lookup = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_operator}"}
    )
    results = json.loads(lookup.data)
    uuid = list(results.keys())[0]

    response = client.put(
        f"/api/v1/services/{uuid}",
        headers={
            "Authorization": f"Basic {valid_operator}",
            "Content-Type": "application/json",
        },
        data=json.dumps(valid_put),
    )
    assert response.status_code == 403


def test_patch_services_unauthorized(client):
    lookup = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_operator}"}
    )
    results = json.loads(lookup.data)
    uuid = list(results.keys())[0]

    response = client.patch(
        f"/api/v1/services/{uuid}",
        headers={
            "Authorization": f"Basic {valid_operator}",
            "Content-Type": "application/json",
        },
        data=json.dumps(valid_patch),
    )
    assert response.status_code == 403


def test_delete_services_unauthorized(client):
    lookup = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_operator}"}
    )
    results = json.loads(lookup.data)
    uuid = list(results.keys())[0]

    response = client.delete(
        f"/api/v1/services/{uuid}",
        headers={
            "Authorization": f"Basic {valid_operator}",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 403


# Verify invalid fields are NOT allowed in requests
#  The following tests are for proper working API calls
def test_post_services_fields_checked_01(client):
    response = client.post(
        "/api/v1/services",
        headers={
            "Authorization": f"Basic {valid_customer}",
            "Content-Type": "application/json",
        },
        data=json.dumps(invalid_post),
    )
    assert response.status_code == 400


def test_put_services_fields_checked_01(client):
    lookup = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_operator}"}
    )
    results = json.loads(lookup.data)
    uuid = list(results.keys())[0]

    response = client.put(
        f"/api/v1/services/{uuid}",
        headers={
            "Authorization": f"Basic {valid_sysadmin}",
            "Content-Type": "application/json",
        },
        data=json.dumps(invalid_put),
    )
    assert response.status_code == 400


def test_patch_services_fields_checked_01(client):
    lookup = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_operator}"}
    )
    results = json.loads(lookup.data)
    uuid = list(results.keys())[0]

    response = client.patch(
        f"/api/v1/services/{uuid}",
        headers={
            "Authorization": f"Basic {valid_sysadmin}",
            "Content-Type": "application/json",
        },
        data=json.dumps(invalid_patch_status),
    )
    assert response.status_code == 400


# TEST Status Options
def test_status_options_good(client):
    lookup = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_operator}"}
    )
    results = json.loads(lookup.data)
    uuid = list(results.keys())[0]

    for status in valid_status:
        print(f"Checking status '{status}'")
        response = client.patch(
            f"/api/v1/services/{uuid}",
            headers={
                "Authorization": f"Basic {valid_sysadmin}",
                "Content-Type": "application/json",
            },
            data=json.dumps({"status": status}),
        )
        assert response.status_code == 204


def test_status_options_bad(client):
    lookup = client.get(
        "/api/v1/services", headers={"Authorization": f"Basic {valid_operator}"}
    )
    results = json.loads(lookup.data)
    uuid = list(results.keys())[0]

    for status in invalid_status:
        print(f"Checking status '{status}'")
        response = client.patch(
            f"/api/v1/services/{uuid}",
            headers={
                "Authorization": f"Basic {valid_sysadmin}",
                "Content-Type": "application/json",
            },
            data=json.dumps({"status": status}),
        )
        assert response.status_code == 400
