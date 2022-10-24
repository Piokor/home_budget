import json
from unittest import mock

import pytest
from mongoengine import connect, disconnect

from home_budget import app
from home_budget.db.users import User

mock_headers = {"x-access-tokens": "1"}


@pytest.fixture
def mock_app():
    app.config.update({
        "TESTING": True,
    })
    disconnect()
    connect('mongoenginetest', host='mongomock://localhost')
    yield app
    disconnect()


@pytest.fixture
def mock_current_user():
    current_user = User(name="username", password="password").save()
    with mock.patch('home_budget.auth.jwt.decode') as decode_mock:
        decode_mock.return_value = {"id": str(current_user.id)}
        yield current_user


def send_post_request(client, endpoint, data):
    return client.post(
        endpoint,
        headers=mock_headers,
        content_type='application/json',
        data=json.dumps(data)
    )


def send_get_request(client, endpoint, args):
    return client.get(
        endpoint,
        headers=mock_headers,
        query_string=args
    )
