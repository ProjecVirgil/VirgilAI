"""Test file."""

import requests

def test_default():
    """Function test."""
    foo = 1
    bar = 1
    assert foo == bar

BASE_URL = "http://127.0.0.1:8080"

def test_call_api_models_ita():
    """Function test api-models."""
    r = requests.get(BASE_URL + "/q/it/Che tempo fa domani a Salerno")
    assert {"Classes predicted":"MT"} == r.json()

def test_call_api_models_en():
    """Function test api-models."""
    r = requests.get(BASE_URL + "/q/en/The weather tomorrow in Salerno")
    assert {"Classes predicted":"MT"} == r.json()
