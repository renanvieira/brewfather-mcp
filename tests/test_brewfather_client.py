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
    FermentableDetail,
    FermentableList,
    HopDetail,
    HopList,
    YeastDetail,
    YeastList,
)


async def mock_make_request(self: BrewfatherInventoryClient, url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=self.auth)
        return response.text


@pytest.fixture
def brewfather_client() -> BrewfatherInventoryClient:
    """Create a BrewfatherInventoryClient instance with mock credentials."""
    client = BrewfatherInventoryClient()
    return client


class TestFermentables:
    @pytest.mark.asyncio
    @pytest.mark.vcr
    async def test_get_fermentables_list(
        self, brewfather_client: BrewfatherInventoryClient
    ):
        with patch.object(
            BrewfatherInventoryClient, "_make_request", mock_make_request
        ):
            result = await brewfather_client.get_fermentables_list()
            assert isinstance(result, FermentableList)
            assert len(result.root) > 0
            assert result.root[0].name is not None
            assert result.root[0].id is not None

    @pytest.mark.asyncio
    @pytest.mark.vcr
    async def test_get_fermentables_detail(
        self, brewfather_client: BrewfatherInventoryClient
    ):
        with patch.object(
            BrewfatherInventoryClient, "_make_request", mock_make_request
        ):
            result = await brewfather_client.get_fermentable_detail(
                "default-0aa30343c0c"
            )
            assert isinstance(result, FermentableDetail)
            assert result.name is not None
            assert result.id is not None
            assert result.inventory >= 0


class TestHops:
    @pytest.mark.asyncio
    @pytest.mark.vcr
    async def test_get_hops_list(self, brewfather_client: BrewfatherInventoryClient):
        with patch.object(
            BrewfatherInventoryClient, "_make_request", mock_make_request
        ):
            result = await brewfather_client.get_hops_list()
            assert isinstance(result, HopList)
            assert len(result.root) > 0
            assert result.root[0].name is not None
            assert result.root[0].id is not None
            assert result.root[0].alpha > 0.0

    @pytest.mark.asyncio
    @pytest.mark.vcr
    async def test_get_hop_detail(self, brewfather_client: BrewfatherInventoryClient):
        with patch.object(
            BrewfatherInventoryClient, "_make_request", mock_make_request
        ):
            result = await brewfather_client.get_hop_detail("default-8e9450d5")
            assert isinstance(result, HopDetail)
            assert result.name is not None
            assert result.id is not None
            assert result.alpha > 0


class TestYeasts:
    @pytest.mark.asyncio
    @pytest.mark.vcr
    async def test_get_yeasts_list(self, brewfather_client: BrewfatherInventoryClient):
        with patch.object(
            BrewfatherInventoryClient, "_make_request", mock_make_request
        ):
            result = await brewfather_client.get_yeasts_list()
            assert isinstance(result, YeastList)
            assert len(result.root) > 0
            assert result.root[0].name is not None
            assert result.root[0].id is not None
            assert result.root[0].attenuation > 0.0

    @pytest.mark.asyncio
    @pytest.mark.vcr
    async def test_get_yeast_detail(self, brewfather_client: BrewfatherInventoryClient):
        with patch.object(
            BrewfatherInventoryClient, "_make_request", mock_make_request
        ):
            result = await brewfather_client.get_yeast_detail("default-016efc")
            assert isinstance(result, YeastDetail)
            assert result.name is not None
            assert result.id is not None
            assert result.attenuation > 0
