import json
import base64

from .utility import client, json_of_response, get_json, post_json

sale_record = {
    "product_name": "Dell XPS 13",
    "items_sold": "1"
}


def test_attendant_can_create_sale_record(client):
    """
    Test if the store attendant can create a new sale record
    """
    product = {

        "product_name": "Dell XPS 13",
        "product_price": "098",
        "instock": "8",
        "max_purchasable": "9",
        "cat_id": "0"

    }
    credentials = base64.b64encode(b'david398:David2018$$').decode('utf-8')
    response = post_json(client, '/api/v1/products', product, credentials)

    credentials = base64.b64encode(b'julius2018:Julius2018@').decode('utf-8')
    response = post_json(client, '/api/v1/sales', sale_record, credentials)
    assert response.status_code == 201
    assert json_of_response(response) == {'message': 'New Sale record created'}


def test_admin_cannot_create_sale_record(client):
    """
    Test admin not allowed to create a new sale record
    """
    sale_record = {
        "product_name": "Dell XPS 13",
        "items_sold": "1"
    }

    credentials = base64.b64encode(b'david398:David2018$$').decode('utf-8')
    response = post_json(client, '/api/v1/sales', sale_record, credentials)
    assert response.status_code == 401
    assert json_of_response(response) == {'error': 'Not authorised to access'}


def test_only_admin_can_access_sale_records(client):
    """
    Test only the admin/store owner can acces all the sale records
    """
    credentials = base64.b64encode(b'david398:David2018$$').decode('utf-8')
    response = get_json(client, '/api/v1/sales', credentials)
    assert response.status_code == 200

    auth = base64.b64encode(b'julius@gmail.com:Julius2018@').decode('utf-8')
    response = get_json(client, '/api/v1/sales', auth)
    assert response.status_code == 401


def test_only_admin_can_access_sale_records(client):
    """
    Test only the admin/store owner can acces all the sale records
    """
    credentials = base64.b64encode(b'david398:David2018$$').decode('utf-8')
    response = get_json(client, '/api/v1/sales', credentials)
    assert response.status_code == 200

    auth = base64.b64encode(b'julius2018:julius').decode('utf-8')
    response = get_json(client, '/api/v1/sales', auth)
    assert response.status_code == 401


def test_admin_can_access_a_sale_record(client):
    """
    Test admin/store owner can get a specific sale using sale_id
    """
    credentials = base64.b64encode(b'david398:David2018$$').decode('utf-8')
    response = get_json(client, '/api/v1/sales/1', credentials)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200


def test_only_creator_of_sale_record_can_access_it(client):
    """
    Test only the creator of a sale record can access his/her sale record

    """
    credentials = base64.b64encode(b'julius2018:Julius2018@').decode('utf-8')
    response = get_json(client, '/api/v1/sales/2', credentials)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 404
    assert json_of_response(response) == {'error': 'sale record not found'}

    response = get_json(client, '/api/v1/sales/1', credentials)
    assert response.status_code == 200
