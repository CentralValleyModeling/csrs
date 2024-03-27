import pytest
import requests


def get_json(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def put_json(url: str, json):
    response = requests.put(url, json=json)
    response.raise_for_status()
    return response.json()


@pytest.fixture
def base_url() -> str:
    return "http://127.0.0.1:8000"


def test_add_assumption(base_url: str):
    assumption = {"name": "example", "detail": "this is an example assumption"}
    response = put_json(base_url + "/assumptions/tucp", assumption)
    assert response["id"] == 1


def test_get_assumption(base_url: str):
    responses = get_json(base_url + "/assumptions/tucp")
    assert len(responses) == 1
    assert responses[0]["id"] == 1
