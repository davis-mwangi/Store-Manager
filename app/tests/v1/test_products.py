import json
import base64

from .utility import client, json_of_response, get_json, post_json

product = {

    "product_name": "Dell XPS 13",
    "product_price": "098",
    "instock": "8",
    "max_purchasable": "9",
    "cat_id": "0"

}


def test_admin_can_add_product(client):
    """
    Test if admin can add a product to the store
    """

    credentials = base64.b64encode(b'david398:David2018$$').decode('utf-8')
    response = post_json(client, '/api/v1/products', product, credentials)
    assert response.status_code == 201
    assert json_of_response(response) == {'message': 'New product created'}


def test_products_exists_error(client):
    """
    Test if users creates a product that already exists
    """
    credentials = base64.b64encode(b'david398:David2018$$').decode('utf-8')
    response = post_json(client, '/api/v1/products', product, credentials)
    response = post_json(client, '/api/v1/products', product, credentials)
    assert response.status_code == 400
    assert json_of_response(response) == {'message': 'Product Already exists'}


def test_attendant_cannot_create_product(client):
    """
    Test that only the admin can create a product \
    """
    credentials = base64.b64encode(b'julius2018:Julius2018@').decode('utf-8')
    response = post_json(client, '/api/v1/products', product, credentials)
    assert response.status_code == 401
    assert json_of_response(response) == {
        'message': 'Not authorised to access '}


def test_get_products(client):
    """
    Test for a successful fetch of products 200 (ok) and
    list length of the retrieved products is equal to default length of 2
    """
    credentials = base64.b64encode(b'david398:David2018$$').decode('utf-8')
    response = get_json(client, '/api/v1/products', credentials)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert len(data['products']) == 1


def test_get_one_product(client):
    """
    Test if sucessfull fetch of a single product status code 200 (OK)
    if the response contains the contents of the product retrieved
    """
    credentials = base64.b64encode(b'david398:David2018$$').decode('utf-8')
    response = post_json(client, '/api/v1/products', product, credentials)

    response = get_json(client, '/api/v1/products/1', credentials)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200


def test_returns_error_for_product_not_found(client):
    """
    Test if the supplied product id does not exist, responds with 404
    and the error message
    """
    credentails = base64.b64encode(b'david398:David2018$$').decode('utf-8')
    response = get_json(client, '/api/v1/products/4', credentails)
    assert response.status_code == 404
    assert json_of_response(response) ==  \
        {"error": "Product with id 4 is not found"}


def test_unregistered_user_cannot_access_resources(client):
    """
    Test only registered users can access the endpoints \
    sample out get '/products' endpoint
    """
    credentials = base64.b64encode(b'ayub2018:david').decode('utf-8')
    response = get_json(client, '/api/v1/sales', credentials)
    assert response.status_code == 401
    assert json_of_response(response) == {'message': 'Access denied'}
