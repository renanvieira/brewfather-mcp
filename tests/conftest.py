from dotenv import load_dotenv
import pytest
import httpx
from pathlib import Path

_ = load_dotenv()

# Create directories for test fixtures
TESTS_DIR = Path("tests")
FIXTURES_DIR = TESTS_DIR / "fixtures"

for directory in [TESTS_DIR, FIXTURES_DIR, FIXTURES_DIR / "vcr_cassettes"]:
    directory.mkdir(exist_ok=True)

# Add pytest-asyncio configuration
pytest_plugins = ["pytest_asyncio"]


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


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [("authorization", "<auth>")],
    }
