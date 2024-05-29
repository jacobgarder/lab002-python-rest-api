def test_get_homepage(client):
    response = client.get("/")
    assert b"Network Service Request" in response.data
    assert response.status_code == 200
