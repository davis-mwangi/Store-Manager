import json
import base64

from .utility import client, json_of_response, get_json, post_json


def test_register_attendant(client):
    """
    Test whether the response code is 201(created)and the json \
    response is 'New user Created Successfully'
    when a new attendant is created
    """
    user_data = {
        "name": "agness wanjiru",
        "email": "agness@gmail.com",
        "username": "agness2018",
        "password": "agness"
    }
    credentials = base64.b64encode(b'david398:david').decode('utf-8')
    response = post_json(client, '/api/v1/register', user_data, credentials)
    assert response.status_code == 201
    assert json_of_response(response) == {"message": "New user" +
                                          " created successfully"}


def test_admin_add_existing_attendant(client):
    """
    Tests if systems gives error if admin  creates a user that already \
    exists
    """
    user_data = {
        "name": "agness wanjiru",
        "email": "agness@gmail.com",
        "username": "agness2018",
        "password": "agness"
    }
    credentials = base64.b64encode(b'david398:david').decode('utf-8')
    response = post_json(client, '/api/v1/register', user_data, credentials)
    response = post_json(client, '/api/v1/register', user_data, credentials)
    assert response.status_code == 400
    assert json_of_response(response) == {'message': 'store attendant ' +
                                          'already exists'}


def test_only_admin_can_add_attendant(client):
    """
    Test that only the admin or store owner can add attendant
    i.e gives 401 (unauthorised acesss) as well as error message
    """
    user_data = {
        "name": "agness wanjiru",
        "email": "agness@gmail.com",
        "username": "agness2018",
        "password": "agness"
    }
    credentials = base64.b64encode(b'julius2018:julius').decode('utf-8')
    response = post_json(client, '/api/v1/register', user_data, credentials)
    assert response.status_code == 401
    assert json_of_response(response) == {'message': 'Not authorised to acess'}