import requests
import responses

from src.tasks import prefect_task_ex
from src.tasks import projecttask
from testing_fixtures.mock_response import request_response

#
# def test_prefect_task(request_response):
#
#     assert prefect_task_ex.prefect_task_ex.fn() is True


def test_that_a_get_request_returns_response_obj(request_response):

    good_response_returned = False

    obj_returned_from_func_call = projecttask.make_get_request.fn(request_response.url)

    if isinstance(obj_returned_from_func_call, requests.models.Response):
        good_response_returned = True

    assert good_response_returned is True
