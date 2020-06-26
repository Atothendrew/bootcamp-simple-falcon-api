import os

import requests

from hello_world.api import RootURI

API_PORT = os.environ.get("API_PORT", 8000)
API_HOST = os.environ.get("API_HOST", "localhost")
API_URI = f"http://{API_HOST}:{API_PORT}"


def test_hello_world():
    response = requests.get(API_URI)
    response.raise_for_status()
    assert response.text == RootURI.DEFAULT_BODY


def test_db_post():
    fake_json_data = {
        "some-key": "some-val"
    }
    response = requests.post(f"{API_URI}/db",
                             json=fake_json_data)
    response.raise_for_status()
    assert response.json() == fake_json_data
