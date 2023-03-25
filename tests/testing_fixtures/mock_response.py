import pytest
import responses


@pytest.fixture(scope="function")
def request_response():
    with responses.RequestsMock() as req_resp:
        responses.add(
            responses.GET,
            "http://testrequestresponse.com",
            body="test response",
            status=200,
        )

    mock_response = req_resp.get("http://testrequestresponse.com", headers={'Content-Type': 'text/html'})

    return mock_response
