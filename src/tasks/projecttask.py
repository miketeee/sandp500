from prefect import task
import requests


@task(name='Make GET Request')
def make_get_request(url: str):
    if requests.get(url=url).status_code == 200:
        response_obj = requests.get(url=url)
    else:
        raise ValueError

    return response_obj
