import os
import typing
import httpx
import pytest
import vcr
from pathlib import Path
from unittest.mock import patch

from vcr.config import RecordMode

from brewfather_mcp.api import BrewfatherInventoryClient
from brewfather_mcp.types import (
    FermentableList,
)


@pytest.fixture
def brewfather_client() -> BrewfatherInventoryClient:
    """Create a BrewfatherInventoryClient instance with mock credentials."""
    client = BrewfatherInventoryClient()
    return client


class TestBrewfatherInventoryClient:
    @pytest.mark.asyncio
    @pytest.mark.vcr
    async def test_get_fermentables_list(
        self, brewfather_client: BrewfatherInventoryClient
    ):
        async def mock_make_request(self: BrewfatherInventoryClient, url: str):
            async with httpx.AsyncClient() as client:
                response = await client.get(url, auth=self.auth)
                return response.text

        with patch.object(
            BrewfatherInventoryClient, "_make_request", mock_make_request
        ):
            result = await brewfather_client.get_fermentables_list()
            assert isinstance(result, FermentableList)
            assert len(result.root) > 0
            assert result.root[0].name is not None
            assert result.root[0].id is not None
