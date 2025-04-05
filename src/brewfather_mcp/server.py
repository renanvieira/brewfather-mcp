import asyncio
from itertools import batched
import logging
from typing import Callable

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Message
from mcp.types import TextContent

from brewfather_mcp.api import BrewfatherInventoryClient
from brewfather_mcp.inventory import (
    get_fermentables_summary,
    get_hops_summary,
    get_yeast_summary,
)
from brewfather_mcp.types import FermentableDetail
from brewfather_mcp.utils import AnyDictList, get_in_batches

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="/tmp/application.log",  # Path to log file
    filemode="a",
)

logger = logging.getLogger(__name__)

mcp = FastMCP("BrewfatherMCP")

_ = load_dotenv()

brewfather_client = BrewfatherInventoryClient()


@mcp.prompt(
    name="Possible beer styles based on inventory",
    description="Ask to list all the possible BJCP styles based on the inventory.",
)
async def styles_based_inventory_prompt() -> list[Message]:
    assistant = Message(
        content=TextContent(
            type="text",
            text="""You are an experienced homebrewer with deep knowledge of the brewing process, ingredients and styles.
            You are not focused on give a full recipe, just an overview of what is possible, which ingredients we already have in the inventory and why given the inventory and by acquiring extra  ingredients.
            """,
        ),
        role="assistant",
    )
    role = "user"
    content = TextContent(
        type="text",
        text="""What are the styles I can brew with my Brewfather inventary?
        Don't be limit to the items in the inventory, but try to use as much as possible from the inventory.
        Use styles from the latest BJCP.
        """,
    )

    return [assistant, Message(content, role=role)]


@mcp.resource(
    uri="inventory://categories",
    name="Inventory Categories",
    description="Lists the available inventory categories.",
)
async def inventory_categories() -> str:
    content = """
    Fermentables (Grains, Adjuncts, etc..)
    Hops
    Yeasts
    """

    return content


@mcp.resource(
    uri="inventory://fermentables",
    name="Fermentables",
    description="List all the fermentables (malts, adjuncts, grains, etc) inventory.",
)
async def read_fermentables() -> str:
    try:
        data = await brewfather_client.get_fermentables_list()

        formatted_response: list[str] = []
        for item in data.root:
            formatted = f"""Name: {item.name}
Type: {item.type}
Supplier: {item.supplier}
Quantity: {item.inventory} kg
Identifier: {item.id}
"""

            formatted_response.append(formatted)

        return "---\n".join(formatted_response)
    except Exception:
        logger.exception("Error happened")
        raise


@mcp.resource(
    uri="inventory://fermentables/{identifier}",
    name="Fermentable detail",
    description="Detailed information of the fermentable item.",
)
async def read_fermentable_detail(identifier: str) -> str:
    logger.info("received request")

    try:
        item = await brewfather_client.get_fermentable_detail(identifier)

        formatted_response = f"""Name: {item.name}
Type: {item.type}
Supplier: {item.supplier}
Inventory: {item.inventory}
Origin: {item.origin}
Grain Category: {item.grain_category}
Potential: {item.potential}
Potential Percentage: {item.potential_percentage}
Color: {item.color}
Moisture: {item.moisture}
Protein: {item.protein}
Diastatic Power: {item.diastatic_power}
Friability: {item.friability}
Not Fermentable: {item.not_fermentable}
Max In Batch: {item.max_in_batch}
Coarse Fine Diff: {item.coarse_fine_diff}
Percent Extract Fine-Ground Dry Basis (FGDB): {item.fgdb}
Hidden: {item.hidden}
Notes: {item.notes}
User Notes: {item.user_notes}
Used In: {item.used_in}
Substitutes: {item.substitutes}
Cost Per Amount: {item.cost_per_amount}
Best Before Date: {item.best_before_date}
Manufacturing Date: {item.manufacturing_date}
Free Amino Nitrogen (FAN): {item.fan}
Percent Coarse-Ground Dry Basic (CGDB): {item.cgdb}
Acid: {item.acid}
ID: {item.id}
"""

        return formatted_response

    except Exception:
        logger.exception("Error happened")
        raise


@mcp.resource(uri="inventory://hops")
async def read_hops() -> str:
    logger.info("received request")

    try:
        data = await brewfather_client.get_hops_list()

        formatted_response: list[str] = []
        for item in data.root:
            formatted = f"""Identifier: {item.id}
Alpha Acids (A.A): {item.alpha}
Quantity: {item.inventory} grams
Name: {item.name}
Type: {item.type}
Use: {item.use}
"""

            formatted_response.append(formatted)

        return "---\n".join(formatted_response)
    except Exception:
        logger.exception("Error happened")
        raise


@mcp.resource(uri="inventory://hops/{identifier}")
async def read_hops_detail(identifier: str) -> str:
    logger.info("received request")

    try:
        item = await brewfather_client.get_hop_detail(identifier)

        formatted = f"""Name: {item.name}
Type: {item.type}
Origin: {item.origin}
Use: {item.use}
Usage: {item.usage}
Alpha Acid (% A.A): {item.alpha}
Beta: {item.beta}
Inventory: {item.inventory}
Time: {item.time}
IBU: {item.ibu}
Oil: {item.oil}
Myrcene: {item.myrcene}
Caryophyllene: {item.caryophyllene}
Humulene: {item.humulene}
Cohumulone: {item.cohumulone}
Farnesene: {item.farnesene}
HSI: {item.hsi}
Year: {item.year}
Temp: {item.temp}
Amount: {item.amount}
Substitutes: {item.substitutes}
Used In: {item.used_in}
Notes: {item.notes}
User Notes: {item.user_notes}
Hidden: {item.hidden}
Best Before Date: {item.best_before_date}
Manufacturing Date: {item.manufacturing_date}
Version: {item.version}
ID: {item.id}
"""
        return formatted

    except:
        logger.exception("Error happened")
        raise


@mcp.resource(uri="inventory://yeasts")
async def read_yeasts() -> str:
    logger.info("received request")

    try:
        data = await brewfather_client.get_yeasts_list()

        formatted_response: list[str] = []
        for item in data.root:
            formatted = f"""Identifier: {item.id}
Attenuation (%): {item.attenuation}
Quantity: {item.inventory} packets
Name: {item.name}
Type: {item.type}
"""

            formatted_response.append(formatted)

        return "---\n".join(formatted_response)
    except:
        logger.exception("Error happened")
        raise


@mcp.resource(uri="inventory://yeasts/{identifier}")
async def read_yeasts_detail(identifier: str) -> str:
    logger.info("received request")

    try:
        item = await brewfather_client.get_yeast_detail(identifier)

        formatted = f"""Name: {item.name}
Type: {item.type}
Form: {item.form}
Laboratory: {item.laboratory}
Product ID: {item.product_id}
Inventory: {item.inventory}
Amount: {item.amount}
Unit: {item.unit}
Attenuation: {item.attenuation}
Min Attenuation: {item.min_attenuation}
Max Attenuation: {item.max_attenuation}
Flocculation: {item.flocculation}
Min Temp: {item.min_temp}
Max Temp: {item.max_temp}
Max ABV: {item.max_abv}
Cells Per Package: {item.cells_per_pkg}
Age Rate: {item.age_rate}
Ferments All: {item.ferments_all}
Description: {item.description}
User Notes: {item.user_notes}
Hidden: {item.hidden}
Best Before Date: {item.best_before_date}
Manufacturing Date: {item.manufacturing_date}
Timestamp: {item.timestamp.seconds}
Created: {item.created.seconds}
Version: {item.version}
ID: {item.id}
Rev: {item.rev}
"""
        return formatted

    except Exception:
        logger.exception("Error happened")
        raise


@mcp.tool()
@mcp.resource(
    uri="inventory://overview",
    name="Brewfather Inventory Overview",
    description="Overview of all the inventory(malts, grains, hops and yeasts). Contains the same data as the PDF/Print export from the app.",
)
async def inventory_summary() -> str:
    try:
        ctx = mcp.get_context()
        fermentables_coro = get_fermentables_summary(brewfather_client)
        hops_coro = get_hops_summary(brewfather_client)
        yeasts_coro = get_yeast_summary(brewfather_client)

        result = await asyncio.gather(fermentables_coro, hops_coro, yeasts_coro)
        await ctx.info("API data gathered")

        fermentables, hops, yeasts = result

        response = "Fermentables:\n\n"
        for fermentable in fermentables:
            for k, v in fermentable.items():
                response += f"{k}: {v}\n"
            response += "\n"

        response += "\n---\n"

        response += "Hops:\n\n"
        for hop in hops:
            for k, v in hop.items():
                response += f"{k}: {v}\n"

        response += "\n---\n"

        response += "Yeasts:\n\n"
        for yeast in yeasts:
            for k, v in yeast.items():
                response += f"{k}: {v}\n"
            response += "\n"

        await ctx.report_progress(100, 100)
        return response
    except Exception:
        logger.exception("Failed to show inventory summary")
        raise
