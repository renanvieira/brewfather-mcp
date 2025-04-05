import os

import httpx

from brewfather_mcp.types import (
    FermentableDetail,
    FermentableList,
    HopDetail,
    HopList,
    InventoryCategory,
    ListQueryParams,
    YeastDetail,
    YeastList,
)

BASE_URL: str = "https://api.brewfather.app/v2"


class BrewfatherInventoryClient:
    __prefix: str = "/inventory"
    __base_url: str = f"{BASE_URL}{__prefix}"
    __inventory_summary_url: str = f"{__base_url}/{{category}}"
    __inventory_detail_url: str = f"{__base_url}/{{category}}/{{id}}"

    auth: httpx.BasicAuth

    def __init__(self):
        user_id = os.getenv("BREWFATHER_API_USER_ID")
        api_key = os.getenv("BREWFATHER_API_KEY")

        if not user_id or not api_key:
            raise ValueError(
                "Missing Brewfather credentials in the environment variables: BREWFATHER_API_USER_ID or BREWFATHER_API_KEY"
            )

        self.auth = httpx.BasicAuth(user_id, api_key)

    async def _make_request(self, url: str) -> str:
        async with httpx.AsyncClient(auth=self.auth) as client:
            response = await client.get(url)
            return response.text

    async def get_fermentables_list(
        self, query_params: ListQueryParams | None = None
    ) -> FermentableList:
        url = self.__inventory_summary_url.format(
            category=InventoryCategory.FERMENTABLES
        )

        if query_params:
            url += f"?{query_params.as_query_param_str()}"

        json_response = await self._make_request(url)
        return FermentableList.model_validate_json(json_response)

    async def get_fermentable_detail(self, id: str) -> FermentableDetail:
        url = self.__inventory_detail_url.format(
            category=InventoryCategory.FERMENTABLES, id=id
        )
        json_response = await self._make_request(url)
        return FermentableDetail.model_validate_json(json_response)

    async def get_hops_list(
        self, query_params: ListQueryParams | None = None
    ) -> HopList:
        url = self.__inventory_summary_url.format(category=InventoryCategory.HOPS)

        if query_params:
            url += f"?{query_params.as_query_param_str()}"

        json_response = await self._make_request(url)
        return HopList.model_validate_json(json_response)

    async def get_hop_detail(self, id: str) -> HopDetail:
        url = self.__inventory_detail_url.format(category=InventoryCategory.HOPS, id=id)
        json_response = await self._make_request(url)
        return HopDetail.model_validate_json(json_response)

    async def get_yeasts_list(
        self, query_params: ListQueryParams | None = None
    ) -> YeastList:
        url = self.__inventory_summary_url.format(category=InventoryCategory.YEASTS)

        if query_params:
            url += f"?{query_params.as_query_param_str()}"

        json_response = await self._make_request(url)
        return YeastList.model_validate_json(json_response)

    async def get_yeast_detail(self, id: str) -> YeastDetail:
        url = self.__inventory_detail_url.format(
            category=InventoryCategory.YEASTS, id=id
        )
        json_response = await self._make_request(url)
        return YeastDetail.model_validate_json(json_response)
