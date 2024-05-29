from flask import session


def test_get_login(client):
    response = client.get("/login")
    assert b"Username" in response.data
    assert response.status_code == 200


def test_login_user(client, operator):
    with client:
        response = client.post(
            "/login",
            data={"username": operator["username"], "password": operator["password"]},
            follow_redirects=True,
        )
        assert f"Hello {operator['username']}" in response.get_data(as_text=True)
        assert response.status_code == 200
        assert session["username"] == operator["username"]
        assert session["authenticated"]


def test_invalid_login(client, operator):
    with client:
        response = client.post(
            "/login",
            data={"username": operator["username"], "password": "badpassword"},
            follow_redirects=True,
        )
        assert f"Hello {operator['username']}" not in response.get_data(as_text=True)
        assert response.status_code == 200
        assert session.get("username") is None


def test_logout(client, operator):
    with client:
        response = client.get("/logout", follow_redirects=True)
        assert f"Hello {operator['username']}" not in response.get_data(as_text=True)
        assert response.status_code == 200
        assert session.get("username") is None


# TODO: Test to verify access to proflie page requires authentication
# TODO: Test to verify contents of profile page is correct
