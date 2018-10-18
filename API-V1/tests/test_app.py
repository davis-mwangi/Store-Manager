import json
import pytest
import base64


from app.app import app


@pytest.fixture
def client(request):
    test_client = app.test_client()

    def teardown():
        pass

    request.addfinalizer(teardown)
    return test_client

# Helper functions for encoding and decoding jsons


def post_json(client, url, json_dict, login_credentials):
    """
    Send  dictionary json_dict as a json to the specified url
    """
    return client.post(url, data=json.dumps(json_dict),
                       content_type='application/json',
                       headers={'Authorization': 'Basic ' + login_credentials})


def get_json(client, url, credentials):
    """Authorize and get json"""
    return client.get(url, headers={'Authorization': 'Basic ' + credentials})


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


def test_register_attendant(client):
    """
    Test whether the response code is 201(created)and the json \
    response is 'New user Created Successfully'
    when a new attendant is created
    """
    user_data = {
        'first_name': 'agness',
        'last_name': 'wanjiru',
        'email': 'agness@gmail.com',
        'password': 'agness',
        'age': 34
    }
    credentials = base64.b64encode(b'david@gmail.com:david').decode('utf-8')
    response = post_json(client, '/api/v1/register', user_data, credentials)
    assert response.status_code == 201
    assert json_of_response(response) == {"message": "New user" +
                                          " created successfully"}


def test_admin_can_add_product(client):
    """
    Test if admin can add a product to the store
    """
    product = {
        "product_name": "macbook pro",
        "price": 70000,
        "instock": 5,
        "category": "computers"
    }
    credentials = base64.b64encode(b'david@gmail.com:david').decode('utf-8')
    response = post_json(client, '/api/v1/products', product, credentials)
    assert response.status_code == 201
    assert json_of_response(response) == {'message': 'New product created'}


def test_get_products(client):
    """
    Test for a successful fetch of products 200 (ok) and
    list length of the retrieved products is equal to default length of 2
    """
    credentials = base64.b64encode(b'david@gmail.com:david').decode('utf-8')
    response = get_json(client, '/api/v1/products', credentials)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert len(data['products']) == 2
