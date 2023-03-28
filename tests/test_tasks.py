import requests
import responses
from testing_fixtures.fixtures import mock_response

from src.tasks import dataextractiontasks


def test_that_a_get_request_returns_response_obj(mock_response):

    good_response_returned = False
    obj_returned_from_func_call = projecttasks.make_get_request.fn(mock_response.url)

    if isinstance(obj_returned_from_func_call, requests.models.Response):
        good_response_returned = True

    assert good_response_returned is True


# def test_verifying_status_of_response_obj(mock_response):
#
#     mock_response_status = mock_response.status
#
#     response_status = projecttask.get_status_code.fn(mock_response)
#
#     assert response_status == "Status is good"



