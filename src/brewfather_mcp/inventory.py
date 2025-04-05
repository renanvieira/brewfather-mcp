from mcp.server.fastmcp import Context, FastMCP

from brewfather_mcp.api import BrewfatherInventoryClient
from brewfather_mcp.utils import AnyDictList, get_in_batches


async def get_fermentables_summary(
    brewfather_client: BrewfatherInventoryClient,
) -> AnyDictList:
    fermentables_data = await brewfather_client.get_fermentables_list()

    detail_results = await get_in_batches(
        3, fermentables_data.root, brewfather_client.get_fermentable_detail
    )

    fermentables: AnyDictList = []
    for f_data, fermentable_data in zip(
        fermentables_data.root, detail_results, strict=True
    ):
        fermentable_data = await brewfather_client.get_fermentable_detail(f_data.id)

        fermentables.append(
            {
                "Name": f_data.name,
                "Type": f_data.type,
                "Yield": fermentable_data.friability,
                "Lot #": fermentable_data.lot_number,
                "Best Before Date": fermentable_data.best_before_date,
                "Inventory Amount": f"{fermentable_data.inventory} kg",
            }
        )

    return fermentables


async def get_hops_summary(brewfather_client: BrewfatherInventoryClient) -> AnyDictList:
    hops_data = await brewfather_client.get_hops_list()
    detail_results = await get_in_batches(
        3, hops_data.root, brewfather_client.get_hop_detail
    )

    hops: AnyDictList = []
    for h_data, hop_data in zip(hops_data.root, detail_results, strict=True):
        hops.append(
            {
                "Name": h_data.name,
                "Year": hop_data.year,
                "Alpha Acid": h_data.alpha,
                "Lot #": hop_data.lot_number,
                "Best Before Date": hop_data.best_before_date,
                "Inventory Amount": f"{hop_data.inventory} grams",
            }
        )

    return hops


async def get_yeast_summary(
    brewfather_client: BrewfatherInventoryClient,
) -> AnyDictList:
    yeasts_data = await brewfather_client.get_yeasts_list()
    detail_results = await get_in_batches(
        3, yeasts_data.root, brewfather_client.get_yeast_detail
    )

    yeasts: AnyDictList = []
    for y_data, yeast_data in zip(yeasts_data.root, detail_results, strict=True):
        yeasts.append(
            {
                "Name": y_data.name,
                "Form": yeast_data.form,
                "Attenuation": f"{y_data.attenuation}%",
                "Lot #": yeast_data.lot_number,
                "Best Before Date": yeast_data.best_before_date,
                "Inventory Amount": f"{yeast_data.inventory} pkg",
            }
        )

    return yeasts
