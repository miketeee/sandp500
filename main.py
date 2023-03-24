from prefect import flow, task
import requests
import responses

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
        )

    mock_response = req_resp.get("http://testrequestresponse.com")
    r = requests.get(url="https://www.google.com")

    print(mock_response.url)



if __name__ == '__main__':
    # print_hi('PyCharm')
    testing()


