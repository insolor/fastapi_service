
def test_messages(client, token):
    response = client.post(
        "/messages",
        headers={"Authorization": "Bearer_" + token},
        json=dict(name="user1", message="Some message"),
    )
    assert response.status_code == 200
    assert response.json() == dict(message="success")
