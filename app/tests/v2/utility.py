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


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))
