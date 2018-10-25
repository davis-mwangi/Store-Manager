import json
import base64

from .utility import client, json_of_response, post_json


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


updated_prod = {
    "product_name": "Safari 2018",
    "product_price": "3000",
    "instock": "20",
    "max_purchasable": "5",
    "cat_id": "1"
}


def test_update_existing_product(client):
    """
    Test updating of product when product exists in the databsae
    """
    response = post_json(client, '/api/v2/products/1', updated_prod,
                         create_mock_token(client))

    assert response.status_code == 200
    assert json_of_response(response) ==  \
        {"message": "Product Updated"}


def test_products_not_found(client):
    """
    Tests when user updates product that doesnt exist
    """
    response = post_json(client, '/api/v2/products/2', updated_prod,
                         create_mock_token(client))

    assert response.status_code == 404
    assert json_of_response(response) ==  \
        {"error": "failed to update, product not found"}
