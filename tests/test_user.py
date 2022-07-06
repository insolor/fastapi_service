

def test_login(client):
    response = client.post(
        "/user/signup",
        json={
            "name": "user1",
            "password": "123"
        }
    )
    assert response.status_code == 200
    assert "token" in response.json()
