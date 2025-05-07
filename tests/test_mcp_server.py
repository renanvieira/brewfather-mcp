# type: ignore

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from brewfather_mcp.server import (
    inventory_categories,
    read_fermentables,
    read_fermentable_detail,
    read_hops,
    read_hops_detail,
    read_yeasts,
    read_yeasts_detail,
    inventory_summary,
    styles_based_inventory_prompt,
)
from brewfather_mcp.api import BrewfatherInventoryClient
from brewfather_mcp.types import (
    FermentableList,
    HopList,
    YeastList,
)


@pytest.fixture
def mock_brewfather_client(mocker):
    mocker.patch("os.getenv", "credential")
    client = AsyncMock(spec=BrewfatherInventoryClient)

    fermentable = MagicMock(
        name="Test Malt",
        type="Grain",
        supplier="Test Supplier",
        inventory=5.0,
        origin="Test Country",
        grain_category="Base",
        potential=1.037,
        potential_percentage=80.0,
        color=3.5,
        moisture=4.0,
        protein=11.0,
        diastatic_power=70,
        friability=80,
        not_fermentable=False,
        max_in_batch=100,
        coarse_fine_diff=1.0,
        fgdb=80,
        hidden=False,
        notes="Test notes",
        user_notes="",
        used_in="",
        substitutes="",
        cost_per_amount=None,
        best_before_date=None,
        manufacturing_date=None,
        fan=None,
        cgdb=None,
        acid=None,
        id="test-id",
    )

    hop = MagicMock(
        name="Test Hop",
        type="Pellet",
        origin="US",
        use="Boil",
        usage="Both",
        alpha=5.5,
        beta=None,
        inventory=100,
        time=60,
        ibu=0,
        oil=None,
        myrcene=None,
        caryophyllene=None,
        humulene=None,
        cohumulone=None,
        farnesene=None,
        hsi=None,
        year=None,
        temp=None,
        amount=None,
        substitutes="",
        used_in="",
        notes="",
        user_notes="",
        hidden=False,
        best_before_date=None,
        manufacturing_date=None,
        version="2.11.6",
        id="test-hop-id",
    )

    yeast = MagicMock(
        name="Test Yeast",
        type="Ale",
        form="Dry",
        laboratory="Test Lab",
        product_id="TY-01",
        inventory=2,
        amount=1,
        unit="pkg",
        attenuation=75,
        min_attenuation=None,
        max_attenuation=None,
        flocculation="Medium",
        min_temp=18,
        max_temp=24,
        max_abv=None,
        cells_per_pkg=None,
        age_rate=None,
        ferments_all=False,
        description="Test yeast description",
        user_notes="",
        hidden=False,
        best_before_date=None,
        manufacturing_date=None,
        timestamp=MagicMock(seconds=1613000000),
        created=MagicMock(seconds=1612000000),
        version="2.10.5",
        id="test-yeast-id",
        rev="abc123",
    )

    fermentables_list = MagicMock(spec=FermentableList)
    fermentables_list.root = [fermentable]
    client.get_fermentables_list.return_value = fermentables_list
    client.get_fermentable_detail.return_value = fermentable

    hops_list = MagicMock(spec=HopList)
    hops_list.root = [hop]
    client.get_hops_list.return_value = hops_list
    client.get_hop_detail.return_value = hop

    yeasts_list = MagicMock(spec=YeastList)
    yeasts_list.root = [yeast]
    client.get_yeasts_list.return_value = yeasts_list
    client.get_yeast_detail.return_value = yeast

    return client


@pytest.fixture
def mock_mcp_context():
    context = AsyncMock()
    context.info = AsyncMock()
    context.report_progress = AsyncMock()
    return context


class TestBrewfatherMCP:
    @pytest.mark.asyncio
    async def test_inventory_categories(self):
        result = await inventory_categories()
        assert "Fermentables" in result
        assert "Hops" in result
        assert "Yeasts" in result

    @pytest.mark.asyncio
    async def test_read_fermentables(self, mock_brewfather_client):
        with patch("brewfather_mcp.server.brewfather_client", mock_brewfather_client):
            result = await read_fermentables()
            assert "Test Malt" in result
            assert "Grain" in result
            assert "5.0 kg" in result

    @pytest.mark.asyncio
    async def test_read_fermentable_detail(self, mock_brewfather_client):
        with patch("brewfather_mcp.server.brewfather_client", mock_brewfather_client):
            result = await read_fermentable_detail("test-id")
            assert "Test Malt" in result
            assert "Test Supplier" in result
            assert "Test Country" in result

    @pytest.mark.asyncio
    async def test_read_hops(self, mock_brewfather_client):
        with patch("brewfather_mcp.server.brewfather_client", mock_brewfather_client):
            result = await read_hops()
            assert "Test Hop" in result
            assert "5.5" in result
            assert "100 grams" in result

    @pytest.mark.asyncio
    async def test_read_hops_detail(self, mock_brewfather_client):
        with patch("brewfather_mcp.server.brewfather_client", mock_brewfather_client):
            result = await read_hops_detail("test-hop-id")
            assert "Test Hop" in result
            assert "Pellet" in result
            assert "US" in result

    @pytest.mark.asyncio
    async def test_read_yeasts(self, mock_brewfather_client):
        with patch("brewfather_mcp.server.brewfather_client", mock_brewfather_client):
            result = await read_yeasts()
            assert "Test Yeast" in result
            assert "75" in result
            assert "2 packets" in result

    @pytest.mark.asyncio
    async def test_read_yeasts_detail(self, mock_brewfather_client):
        with patch("brewfather_mcp.server.brewfather_client", mock_brewfather_client):
            result = await read_yeasts_detail("test-yeast-id")
            assert "Test Yeast" in result
            assert "Test Lab" in result
            assert "Medium" in result

    @pytest.mark.asyncio
    async def test_inventory_summary(self, mock_brewfather_client, mock_mcp_context):
        with (
            patch("brewfather_mcp.server.brewfather_client", mock_brewfather_client),
            patch(
                "brewfather_mcp.server.mcp.get_context", return_value=mock_mcp_context
            ),
            patch(
                "brewfather_mcp.inventory.get_fermentables_summary",
                return_value=[{"Name": "Test Malt", "Inventory": "5.0 kg"}],
            ),
            patch(
                "brewfather_mcp.inventory.get_hops_summary",
                return_value=[{"Name": "Test Hop", "Inventory": "100 g"}],
            ),
            patch(
                "brewfather_mcp.inventory.get_yeast_summary",
                return_value=[{"Name": "Test Yeast", "Inventory": "2 pkg"}],
            ),
        ):
            result = await inventory_summary()
            assert "Fermentables:" in result
            assert "Hops:" in result
            assert "Yeasts:" in result
            assert "Test Malt" in result
            assert "Test Hop" in result
            assert "Test Yeast" in result
            mock_mcp_context.report_progress.assert_called_with(100, 100)

    @pytest.mark.asyncio
    async def test_styles_based_inventory_prompt(self):
        messages = await styles_based_inventory_prompt()
        assert len(messages) == 2
        assert messages[0].role == "assistant"
        assert messages[1].role == "user"
        assert "BJCP" in messages[1].content.text

    @pytest.mark.asyncio
    async def test_error_handling_read_fermentables(self, mock_brewfather_client):
        mock_brewfather_client.get_fermentables_list.side_effect = Exception(
            "API error"
        )
        with (
            patch("brewfather_mcp.server.brewfather_client", mock_brewfather_client),
            patch("brewfather_mcp.server.logger") as mock_logger,
        ):
            with pytest.raises(Exception):
                await read_fermentables()

            mock_logger.exception.assert_called_once()
