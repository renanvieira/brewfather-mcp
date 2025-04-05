import typing
from dotenv import load_dotenv
import pytest

_ = load_dotenv()


@pytest.fixture
def httpx_mock():
    """Return a mock httpx client."""

    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    class MockClient:
        async def get(self, *args, **kwargs):
            # Mock response based on URL
            if "fermentables" in args[0]:
                return MockResponse(
                    [
                        {
                            "_id": "test-id",
                            "name": "Test Fermentable",
                            "type": "Grain",
                            "supplier": "Test Supplier",
                            "inventory": 5.0,
                        }
                    ]
                )
            elif "hops" in args[0]:
                return MockResponse(
                    [
                        {
                            "_id": "test-hop-id",
                            "alpha": 5.5,
                            "inventory": 100,
                            "name": "Test Hop",
                            "type": "Pellet",
                            "use": "Boil",
                        }
                    ]
                )
            elif "yeasts" in args[0]:
                return MockResponse(
                    [
                        {
                            "_id": "test-yeast-id",
                            "attenuation": 75,
                            "inventory": 2,
                            "name": "Test Yeast",
                            "type": "Ale",
                        }
                    ]
                )
            else:
                return MockResponse({}, 404)

    return MockClient()


def remove_response_headers(response: dict[str, typing.Any]):
    """Removes specific headers from response to avoid leaking developers information"""
    if "headers" in response:
        headers_to_remove = [
            "X-Served-By",
            "X-Cloud-Trace-Context",
            "Etag",
            "Date",
            "X-Country-Code",
            "X-Served-By",
            "X-Timer",
        ]  # Specify headers to remove
        for header in headers_to_remove:
            response["headers"].pop(header, None)

    return response


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [("authorization", "Basic dXNlcjpwYXNzd29yZA==")],
        "before_record_response": remove_response_headers,
    }
