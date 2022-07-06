def test_messages(client, token):
    message = dict(name="user1", message="Some message")
    response = client.post(
        "/messages",
        headers={"Authorization": "Bearer_" + token},
        json=message,
    )
    assert response.status_code == 200
    assert response.json() == dict(message="success")

    response = client.post(
        "/messages",
        headers={"Authorization": "Bearer_" + token},
        json=dict(name="user1", message="messages 10"),
    )
    assert response.status_code == 200
    assert response.json() == [message]
