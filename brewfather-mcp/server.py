from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import os
import logging
import sys
import asyncio
import traceback

logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,  # Direct logs to standard output
)
logger = logging.getLogger()

mcp = FastMCP("Brewfather MCP")

load_dotenv()


@mcp.tool()
async def read_fermentables() -> str:
    logger.info("received request")

    try:
        url = "https://api.brewfather.app/v2/inventory/fermentables"
        auth = httpx.BasicAuth(
            os.getenv("BREWFATHER_API_USER_ID"), os.getenv("BREWFATHER_API_KEY")
        )

        client = httpx.AsyncClient(auth=auth)

        response = await client.get(url)
        data = response.json()

        formatted_response = []
        for item in data:
            formatted = f"""
            Name: {item["name"]}
            Type: {item["type"]}
            Supplier: {item["supplier"]}
            Quantity: {item["inventory"]} kg
            Identifier: {item["_id"]}
            """

            formatted_response.append(formatted)

        return "\n---\n".join(formatted_response)
    except:
        logger.exception("Error happened")
        raise


@mcp.tool()
async def read_fermentable_detail(identifier: str) -> str:
    logger.info("received request")

    try:
        url = f"https://api.brewfather.app/v2/inventory/fermentables/{identifier}"
        auth = httpx.BasicAuth(
            os.getenv("BREWFATHER_API_USER_ID"), os.getenv("BREWFATHER_API_KEY")
        )

        client = httpx.AsyncClient(auth=auth)

        response = await client.get(url)
        item = response.json()

        formatted_response = f"""
            Name: {item["name"]}
            Type: {item["type"]}
            Supplier: {item["supplier"]}
            Inventory: {item["inventory"]}
            Origin: {item["origin"]}
            Grain Category: {item["grainCategory"]}
            Potential: {item["potential"]}
            Potential Percentage: {item["potentialPercentage"]}
            Color: {item["color"]}
            Moisture: {item["moisture"]}
            Protein: {item["protein"]}
            Diastatic Power: {item["diastaticPower"]}
            Friability: {item["friability"]}
            Not Fermentable: {item["notFermentable"]}
            Max In Batch: {item["maxInBatch"]}
            Coarse Fine Diff: {item["coarseFineDiff"]}
            Percent Extract Fine-Ground Dry Basis (FGDB): {item["fgdb"]}
            Hidden: {item["hidden"]}
            Notes: {item["notes"]}
            User Notes: {item["userNotes"]}
            Used In: {item["usedIn"]}
            Substitutes: {item["substitutes"]}
            Cost Per Amount: {item["costPerAmount"]}
            Best Before Date: {item["bestBeforeDate"]}
            Manufacturing Date: {item["manufacturingDate"]}
            Free Amino Nitrogen (FAN): {item["fan"]}
            Percent Coarse-Ground Dry Basic (CGDB): {item["cgdb"]}
            Acid: {item["acid"]}
            ID: {item["_id"]}
        """

        return formatted_response

    except:
        logger.exception("Error happened")
        raise


@mcp.tool()
async def read_hops() -> str:
    logger.info("received request")

    try:
        url = "https://api.brewfather.app/v2/inventory/hops"
        auth = httpx.BasicAuth(
            os.getenv("BREWFATHER_API_USER_ID"), os.getenv("BREWFATHER_API_KEY")
        )

        client = httpx.AsyncClient(auth=auth)

        response = await client.get(url)
        data = response.json()

        formatted_response = []
        for item in data:
            formatted = f"""
            Identifier: {item["_id"]}
            Alpha Acids (A.A): {item["alpha"]}
            Quantity: {item["inventory"]} grams
            Name: {item["name"]}
            Type: {item["type"]}
            Use: {item["use"]}
            """

            formatted_response.append(formatted)

        return "\n---\n".join(formatted_response)
    except:
        logger.exception("Error happened")
        raise


@mcp.tool()
async def read_hops_detail(identifier: str) -> str:
    logger.info("received request")

    try:
        url = f"https://api.brewfather.app/v2/inventory/hops/{identifier}"
        auth = httpx.BasicAuth(
            os.getenv("BREWFATHER_API_USER_ID"), os.getenv("BREWFATHER_API_KEY")
        )

        client = httpx.AsyncClient(auth=auth)

        response = await client.get(url)
        item = response.json()

        formatted = f"""
        Name: {item["name"]}
        Type: {item["type"]}
        Origin: {item["origin"]}
        Use: {item["use"]}
        Usage: {item["usage"]}
        Alpha Acid (% A.A): {item["alpha"]}
        Beta: {item["beta"]}
        Inventory: {item["inventory"]}
        Time: {item["time"]}
        IBU: {item["ibu"]}
        Oil: {item["oil"]}
        Myrcene: {item["myrcene"]}
        Caryophyllene: {item["caryophyllene"]}
        Humulene: {item["humulene"]}
        Cohumulone: {item["cohumulone"]}
        Farnesene: {item["farnesene"]}
        HSI: {item["hsi"]}
        Year: {item["year"]}
        Temp: {item["temp"]}
        Amount: {item["amount"]}
        Substitutes: {item["substitutes"]}
        Used In: {item["usedIn"]}
        Notes: {item["notes"]}
        User Notes: {item["userNotes"]}
        Hidden: {item["hidden"]}
        Best Before Date: {item["bestBeforeDate"]}
        Manufacturing Date: {item["manufacturingDate"]}
        Version: {item["_version"]}
        ID: {item["_id"]}
        """
        return formatted

    except:
        logger.exception("Error happened")
        raise


@mcp.tool()
async def read_yeasts() -> str:
    logger.info("received request")

    try:
        url = "https://api.brewfather.app/v2/inventory/yeasts"
        auth = httpx.BasicAuth(
            os.getenv("BREWFATHER_API_USER_ID"), os.getenv("BREWFATHER_API_KEY")
        )

        client = httpx.AsyncClient(auth=auth)

        response = await client.get(url)
        data = response.json()

        formatted_response = []
        for item in data:
            formatted = f"""
            Identifier: {item["_id"]}
            Attenuation (%): {item["attenuation"]}
            Quantity: {item["inventory"]} packets
            Name: {item["name"]}
            Type: {item["type"]}
            """

            formatted_response.append(formatted)

        return "\n---\n".join(formatted_response)
    except:
        logger.exception("Error happened")
        raise


@mcp.tool()
async def read_yeasts_detail(identifier: str) -> str:
    logger.info("received request")

    try:
        url = f"https://api.brewfather.app/v2/inventory/yeasts/{identifier}"
        auth = httpx.BasicAuth(
            os.getenv("BREWFATHER_API_USER_ID"), os.getenv("BREWFATHER_API_KEY")
        )

        client = httpx.AsyncClient(auth=auth)

        response = await client.get(url)
        item = response.json()

        formatted = f"""
        Name: {item.get("name")}
        Type: {item.get("type")}
        Form: {item.get("form")}
        Laboratory: {item.get("laboratory")}
        Product ID: {item.get("productId")}
        Inventory: {item.get("inventory")}
        Amount: {item.get("amount")}
        Unit: {item.get("unit")}
        Attenuation: {item.get("attenuation")}
        Min Attenuation: {item.get("minAttenuation")}
        Max Attenuation: {item.get("maxAttenuation")}
        Flocculation: {item.get("flocculation")}
        Min Temp: {item.get("minTemp")}
        Max Temp: {item.get("maxTemp")}
        Max ABV: {item.get("maxAbv")}
        Cells Per Package: {item.get("cellsPerPkg")}
        Age Rate: {item.get("ageRate")}
        Ferments All: {item.get("fermentsAll")}
        Description: {item.get("description")}
        User Notes: {item.get("userNotes")}
        Hidden: {item.get("hidden")}
        Best Before Date: {item.get("bestBeforeDate")}
        Manufacturing Date: {item.get("manufacturingDate")}
        Timestamp: {item.get("_timestamp")["_seconds"]}
        Created: {item.get("_created")["_seconds"]}
        Version: {item.get("_version")}
        ID: {item.get("_id")}
        Rev: {item["_rev"]}
        """
        return formatted

    except:
        logger.exception("Error happened")
        raise


async def get_fermentables_summary() -> list[dict]:
    url = "https://api.brewfather.app/v2/inventory/fermentables"
    auth = httpx.BasicAuth(
        os.getenv("BREWFATHER_API_USER_ID"), os.getenv("BREWFATHER_API_KEY")
    )

    client = httpx.AsyncClient(auth=auth)

    response = await client.get(url)
    fermentables_data = response.json()

    fermentables = []
    for f_data in fermentables_data:
        url = f"https://api.brewfather.app/v2/inventory/fermentables/{f_data['_id']}"
        response = await client.get(url)
        fermentable_data = response.json()

        fermentables.append(
            {
                "Name": f_data.get("name"),
                "Type": f_data.get("type"),
                "Yield": fermentable_data.get("friability"),
                "Lot #": fermentable_data.get("lotNumber"),
                "Best Before Date": fermentable_data.get("bestBeforeDate"),
                "Inventory Amount": f"{fermentable_data.get('inventory')} kg",
            }
        )

    return fermentables


async def get_hops_summary() -> dict:
    url = "https://api.brewfather.app/v2/inventory/hops"
    auth = httpx.BasicAuth(
        os.getenv("BREWFATHER_API_USER_ID"), os.getenv("BREWFATHER_API_KEY")
    )

    client = httpx.AsyncClient(auth=auth)

    response = await client.get(url)
    hops_data = response.json()

    hops = []
    for h_data in hops_data:
        url = f"https://api.brewfather.app/v2/inventory/hops/{h_data['_id']}"
        response = await client.get(url)
        hop_data = response.json()

        hops.append(
            {
                "Name": h_data.get("name"),
                "Year": hop_data.get("Year"),
                "Alpha Acid": h_data.get("alpha"),
                "Lot #": hop_data.get("lotNumber"),
                "Best Before Date": hop_data.get("bestBeforeDate"),
                "Inventory Amount": f"{hop_data.get('inventory')} grams",
            }
        )

    return hops


async def get_yeast_summary() -> dict:
    url = "https://api.brewfather.app/v2/inventory/yeasts"
    auth = httpx.BasicAuth(
        os.getenv("BREWFATHER_API_USER_ID"), os.getenv("BREWFATHER_API_KEY")
    )

    client = httpx.AsyncClient(auth=auth)

    response = await client.get(url)
    hops_data = response.json()

    hops = []
    for h_data in hops_data:
        url = f"https://api.brewfather.app/v2/inventory/yeasts/{h_data['_id']}"
        response = await client.get(url)
        hop_data = response.json()

        hops.append(
            {
                "Name": h_data.get("name"),
                "Form": hop_data.get("Form"),
                "Attenuation": f"{h_data.get('attenuation')}%",
                "Lot #": hop_data.get("lotNumber"),
                "Best Before Date": hop_data.get("bestBeforeDate"),
                "Inventory Amount": f"{hop_data.get('inventory')} pkg",
            }
        )

    return hops


@mcp.tool()
async def inventory_summary() -> str:
    try:
        fermentables_coro = get_fermentables_summary()
        hops_coro = get_hops_summary()
        yeasts_coro = get_yeast_summary()

        result = await asyncio.gather(fermentables_coro, hops_coro, yeasts_coro)

        fermentables, hops, yeasts = result

        response = "Fermentables:\n\n"
        for fermentable in fermentables:
            for k, v in fermentable.items():
                response += f"{k}: {v}\n"
            response += "\n\n"

        response += "\n---\n"

        response += "Hops:\n\n"
        for hop in hops:
            for k, v in hop.items():
                response += f"{k}: {v}\n"
            response += "\n\n"

        response += "\n---\n"

        response += "Yeasts:\n\n"
        for yeast in yeasts:
            for k, v in yeast.items():
                response += f"{k}: {v}\n"
            response += "\n\n"

        response += "\n---\n"

        return response
    except Exception as e:
        return dict(error=traceback.format_exc())
