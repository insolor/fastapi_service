def test_user(client):
    # Try to create a user with empty password
    response = client.post(
        "/user/signup",
        json=dict(name="user1", password=""),
    )
    assert response.status_code == 400

    # Try to create a user
    response = client.post(
        "/user/signup",
        json=dict(name="user1", password="123"),
    )
    assert response.status_code == 200
    assert "token" in response.json()

    # Try to create the same user again
    response = client.post(
        "/user/signup",
        json=dict(name="user1", password="123"),
    )
    assert response.status_code == 400

    # Test login
    response = client.post(
        "/user/login",
        json=dict(name="user1", password="123"),
    )
    assert response.status_code == 200
    assert "token" in response.json()
