import json

import pytest

from app import app


@pytest.fixture
def client(request):
    test_client = app.test_client()

    def teardown():
        pass

    request.addfinalizer(teardown)
    return test_client


def post_json(client, url, json_dict, token):
    return client.post(url, data=json.dumps(json_dict),
                       content_type='application/json',
                       headers={'Authorization': 'Bearer ' + token})


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))
