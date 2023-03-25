from prefect import flow, task
import requests
import responses
from responses import matchers

@flow(name="My Flow", log_prints=True)
def print_hi(name):

    print(f'Hi, {name}')

def testing():
    with responses.RequestsMock() as req_resp:
        responses.add(
            responses.GET,
            "http://testrequestresponse.com",
            body="test response",
            status=200,
            # headers={'Content-Type': 'text/html'},
        )

    mock_response = req_resp.get("http://testrequestresponse.com", headers={'Content-Type': 'text/html'})
    r = requests.get(url="https://www.google.com")

    # print(r.headers['content-type'].split(';')[0].split('/'))
    print(dir(mock_response))
    print(r.headers['Content_Type'])



if __name__ == '__main__':
    # print_hi('PyCharm')
    testing()


