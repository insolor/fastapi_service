def test_messages(client, user_token):
    user, token = user_token
    message = dict(name=user, message="Some message")
    response = client.post(
        "/messages",
        headers={"Authorization": "Bearer_" + token},
        json=message,
    )
    assert response.status_code == 200, response.text
    assert response.json() == dict(message="success")

    response = client.post(
        "/messages",
        headers={"Authorization": "Bearer_" + token},
        json=dict(name=user, message="messages 10"),
    )
    assert response.status_code == 200
    assert response.json() == [message]
