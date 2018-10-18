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
    assert len(data['products']) == 3


def test_get_one_product(client):
    """
    Test if sucessfull fetch of a single product status code 200 (OK)
    if the response contains the contents of the product retrieved
    """
    credentails = base64.b64encode(b'david@gmail.com:david').decode('utf-8')
    response = get_json(client, '/api/v1/products/1', credentails)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['product'] == {
        'product_id': 1,
        'product_name': 'dell laptop',
        'price': 70000,
        'instock': 5,
        'category': 'computers'
    }


def test_returns_error_for_product_not_found(client):
    """
    Test if the supplied product id does not exist, responds with 404
    and the error message
    """
    credentails = base64.b64encode(b'david@gmail.com:david').decode('utf-8')
    response = get_json(client, '/api/v1/products/4', credentails)
    assert response.status_code == 404
    assert json_of_response(response) ==  \
        {"error": "Product with id 4 is not found"}


def test_attendant_can_create_sale_record(client):
    """
    Test if the store attendant can create a new sale record
    """
    sale_record = {

        "sale_date": "17/10/2018",
        "total_price": 2850,
        "products_sold": [
            {
                "id": 1,
                "product_name": "sugar",
                "price_per_item": 200,
                "items_sold": 10,
                "total_amount": 2000
            }

        ]
    }
    credentials = base64.b64encode(b'julius@gmail.com:julius').decode('utf-8')
    response = post_json(client, '/api/v1/sales', sale_record, credentials)
    assert response.status_code == 201
    assert json_of_response(response) == {'message': 'New Sale record created'}
