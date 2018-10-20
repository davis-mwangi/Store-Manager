import json
import base64

from .utility import client, json_of_response, get_json, post_json


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
    credentials = base64.b64encode(b'julius2018:julius').decode('utf-8')
    response = post_json(client, '/api/v1/sales', sale_record, credentials)
    assert response.status_code == 201
    assert json_of_response(response) == {'message': 'New Sale record created'}


def test_admin_cannot_create_sale_record(client):
    """
    Test admin not allowed to create a new sale record
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
    credentials = base64.b64encode(b'david398:david').decode('utf-8')
    response = post_json(client, '/api/v1/sales', sale_record, credentials)
    assert response.status_code == 401
    assert json_of_response(response) == {'error': 'Not authorised to access'}


def test_only_admin_can_access_sale_records(client):
    """
    Test only the admin/store owner can acces all the sale records
    """
    credentials = base64.b64encode(b'david398:david').decode('utf-8')
    response = get_json(client, '/api/v1/sales', credentials)
    assert response.status_code == 200

    auth = base64.b64encode(b'julius@gmail.com:julius').decode('utf-8')
    response = get_json(client, '/api/v1/sales', auth)
    assert response.status_code == 401


def test_only_admin_can_access_sale_records(client):
    """
    Test only the admin/store owner can acces all the sale records
    """
    credentials = base64.b64encode(b'david398:david').decode('utf-8')
    response = get_json(client, '/api/v1/sales', credentials)
    assert response.status_code == 200

    auth = base64.b64encode(b'julius2018:julius').decode('utf-8')
    response = get_json(client, '/api/v1/sales', auth)
    assert response.status_code == 401


def test_admin_can_access_a_sale_record(client):
    """
    Test admin/store owner can get a specific sale using sale_id
    """
    credentials = base64.b64encode(b'david398:david').decode('utf-8')
    response = get_json(client, '/api/v1/sales/1', credentials)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200


def test_only_creator_of_sale_record_can_access_it(client):
    """
    Test only the creator of a sale record can access his/her sale record

    """
    credentials = base64.b64encode(b'julius2018:julius').decode('utf-8')
    response = get_json(client, '/api/v1/sales/2', credentials)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 404
    assert json_of_response(response) == {'error': 'sale record not found'}

    response = get_json(client, '/api/v1/sales/1', credentials)
    assert response.status_code == 200
