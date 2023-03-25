from prefect import task
import requests


@task(name='Make GET Request')
def make_get_request(url: str):
    if isinstance(requests.get(url=url), requests.models.Response):
        response_obj = requests.get(url=url)
    else:
        raise ValueError

    return response_obj


@task(name='Get status code of response object')
def get_status_code():
    pass

