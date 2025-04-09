import logging
from collections.abc import MutableMapping
from typing import Any
import pytest
import requests


def pytest_tavern_beta_before_every_request(request_args: MutableMapping):
    message = f"Request: {request_args['method']} {request_args['url']}"

    params = request_args.get('params', None)
    if params:
        message += f"\nQuery parameters: {params}"
    
    message += f"\nRequest body: {request_args.get('json', '<no body>')}"

    logging.info(message)


def pytest_tavern_beta_after_every_response(expected: Any, response: Any) -> None:
    logging.info(f"Response: {response.status_code} {response.text}")


@pytest.fixture(autouse=True)
def clear_db():
    resp = requests.get('http://127.0.0.1:8081/ping')
    if resp.status_code != 200:
        pytest.fail(f"Ping not passed with status code {resp.status_code}")
    requests.post('http://127.0.0.1:8081/test/drop-db')
