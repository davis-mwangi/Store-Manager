import json
import base64

from .utility import client, json_of_response


def test_login(client):
    user_data = {
        "username": "david398",
        "password": "David2018$$"
    }
    response = client.post('/api/v2/auth/login', data=json.dumps(user_data),
                           content_type='application/json')
    assert response.status_code == 200


def test_login_error(client):
    """
    Test if user can sign in
    """
    user_data = {
        "username": "david398",
        "password": "wrong_password"
    }
    response = client.post('/api/v2/auth/login', data=json.dumps(user_data),
                           content_type='application/json')
    assert response.status_code == 401
    assert json_of_response(response) == {'message': 'Invalid credentials'}


def test_missing_username(client):
    """
    Test response if user submit blank username field
    """
    user_data = {
        "username": "",
        "password": "wrong_password"
    }
    response = client.post('/api/v2/auth/login', data=json.dumps(user_data),
                           content_type='application/json')
    assert response.status_code == 400
    assert json_of_response(response) == {
        'message': {'username': 'Cannot be blank'}}
