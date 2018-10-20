import pytest
import json
from app import app


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
