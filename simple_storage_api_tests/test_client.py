import os

import requests

from simple_storage_api.api import RootURI

API_PORT = os.environ.get("API_PORT", 8000)
API_HOST = os.environ.get("API_HOST", "localhost")
API_URI = f"http://{API_HOST}:{API_PORT}"


def test_simple_storage_api():
    response = requests.get(API_URI)
    response.raise_for_status()
    assert response.text == RootURI.DEFAULT_BODY


def test_db_post():
    key = os.environ.get("POST_KEY", "I was created from")
    val = os.environ.get("POST_VALUE", "I was created from")
    fake_json_data = {
        key : val
    }
    response = requests.post(f"{API_URI}/db",
                             json=fake_json_data)
    response.raise_for_status()
    response_json = response.json()
    assert key in response_json
    assert val == response_json[key]
