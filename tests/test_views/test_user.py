from ..config import client

def test_users_endpoint_get():
    response = client.get("/users/")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    data = response.json()
    assert isinstance(data, dict)
