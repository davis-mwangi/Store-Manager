import json

from .utility import client, json_of_response, post_json

# ##################### LOGIN ################################


def test_login(client):
    login_data = {
        "username": "david398",
        "password": "David2018$$"
    }
    response = client.post('/api/v2/auth/login', data=json.dumps(login_data),
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


def test_missing_login_username(client):
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
    assert json_of_response(response) == {'message':
                                          {'username': ' Cannot be blank'}}

# ######################## SIGN UP USER ##################################


user_data = {
    "firstname": "testfirstname",
    "lastname": "testlastname",
    "email": "test@gmail.com",
    "password": "Q@aaaaaaa66"
}


def create_mock_token(client):
    mock_login_data = {
        "username": "david398",
        "password": "David2018$$"
    }
    response = client.post('/api/v2/auth/login',
                           data=json.dumps(mock_login_data),
                           content_type='application/json')
    json_response = json_of_response(response)
    token = json_response['access_token']
    return token


def test_add_existing_attendant(client):
    """
    Tests for duplication of username
    """

    response = post_json(client, '/api/v2/auth/signup', user_data,
                         create_mock_token(client))
    assert response.status_code == 400
    assert json_of_response(response) == {'message': 'store attendant ' +
                                          'already exists'}


def test_invalid_email(client):
    """
    Tests if user enter valid email
    """
    incorect_data = {
        "firstname": "testfirstname",
        "lastname": "testlastname",
        "email": "invalid_email",
        "password": "Q@aaaaaaa66"
    }
    response = post_json(client, '/api/v2/auth/signup', incorect_data,
                         create_mock_token(client))
    assert response.status_code == 400
    assert json_of_response(response) == {
        "message": {
            "email": "Invalid email format"
        }
    }


def test_valid_name(client):
    """
    Test if user inputs valid names i.e firstname , lastname
    """
    incorect_data = {
        "firstname": "9087678987",
        "lastname": "^^^&*&*((*",
        "email": "invalid_email",
        "password": "Q@aaaaaaa66"
    }
    response = post_json(client, '/api/v2/auth/signup', incorect_data,
                         create_mock_token(client))
    assert response.status_code == 400
    assert json_of_response(response) == {
        "message": {
            "firstname": "Invalid name"
        }
    }
