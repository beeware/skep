
def test_home(test_client):
    "The home page can be retrieved."
    response = test_client.get('/')
    assert response.status_code == 200
