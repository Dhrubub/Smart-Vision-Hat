def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Smart Vision Hat' in response.data


def test_login_route_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_user_manual_route(client):
    response = client.get('/user_manual')
    assert response.status_code == 200
    assert b'User Manual' in response.data
