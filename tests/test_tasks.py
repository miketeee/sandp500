import requests
import responses
from testing_fixtures.mock_response import request_response

from src.tasks import projecttask


def test_that_a_get_request_returns_response_obj(request_response):

    good_response_returned = False
    obj_returned_from_func_call = projecttask.make_get_request.fn(request_response.url)

    if isinstance(obj_returned_from_func_call, requests.models.Response):
        good_response_returned = True

    assert good_response_returned is True


def test_verifying_status_of_response_obj(request_response):

    response_status = projecttask.get_status_code.fn()

    assert response_status.status == 200



