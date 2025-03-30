import os

import httpx

from brewfather_mcp.types import (
    FermentableDetail,
    FermentablesSummary,
    HopDetail,
    HopList,
    InventoryCategory,
    YeastDetail,
    YeastList,
)

BASE_URL: str = "https://api.brewfather.app/v2"


class BrewfatherInventoryClient:
    __prefix: str = "/inventory"
    __base_url: str = f"{BASE_URL}/{__prefix}"
    __inventory_summary_url: str = f"{__base_url}/{{category}}"
    __inventory_detail_url: str = f"{__base_url}/{{category}}/{{id}}"

    auth: httpx.BasicAuth

    def __init__(self):
        if (
            "BREWFATHER_API_USER_ID" not in os.environ
            or "BREWFATHER_API_KEY" not in os.environ
        ):
            raise ValueError(
                "Missing Brewfather credentials in the environment variables: BREWFATHER_API_USER_ID or BREWFATHER_API_KEY"
            )

        self.auth = httpx.BasicAuth(
            os.getenv("BREWFATHER_API_USER_ID"), os.getenv("BREWFATHER_API_KEY")
        )

    async def _make_request(self, url) -> dict:
        with httpx.AsyncClient as client:
            response = await client.get()
            return response.json()

    async def get_fermentables_list(self) -> FermentablesSummary:
        url = self.__fermentables_summary_url.format(
            category=InventoryCategory.FERMENTABLES
        )
        json_response = self._make_request(url)
        return FermentablesSummary.model_validate_json(json_response)

    async def get_fermentable_detail(self, id: str) -> FermentableDetail:
        url = self.__fermentable_detail_url.format(
            category=InventoryCategory.FERMENTABLES, id=id
        )
        json_response = self._make_request(url)
        return FermentableDetail.model_validate_json(json_response)

    async def get_hops_list(self) -> HopList:
        url = self.__fermentables_summary_url.format(category=InventoryCategory.HOPS)
        json_response = self._make_request(url)
        return HopList.model_validate_json(json_response)

    async def get_hop_detail(self, id: str) -> HopDetail:
        url = self.__fermentable_detail_url.format(
            category=InventoryCategory.HOPS, id=id
        )
        json_response = self._make_request(url)
        return HopDetail.model_validate_json(json_response)

    async def get_yeasts_list(self) -> YeastList:
        url = self.__fermentables_summary_url.format(category=InventoryCategory.YEASTS)
        json_response = self._make_request(url)
        return HopList.model_validate_json(json_response)

    async def get_yeasts_detail(self, id: str) -> YeastDetail:
        url = self.__fermentable_detail_url.format(
            category=InventoryCategory.YEASTS, id=id
        )
        json_response = self._make_request(url)
        return HopDetail.model_validate_json(json_response)
