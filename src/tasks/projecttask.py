from prefect import task, get_run_logger
import requests
from logging.get_logger import task_logger
import inspect


@task(name='Make GET Request')
def make_get_request(url: str):
    response_obj = requests.get(url=url)
    if not isinstance(response_obj, requests.models.Response):
        task_logger().info(
            f"Passed in args: {inspect.getargvalues()}, "
            f"Type of request response: {type(response_obj)}, "
            f"Function caller: {inspect.currentframe()}")
        raise ValueError
    else:
        return response_obj


@task(name='Verify Status is 200')
def get_status_code(response_obj: requests.models.Response):
    if response_obj.status_code == 200:
        return response_obj
    else:
        task_logger().info(f"The request returned a status of {response_obj.status_code}")



