from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import os
import logging
import sys
import asyncio
import traceback
from brewfather_mcp.api import BrewfatherInventoryClient

logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,  # Direct logs to standard output
)
logger = logging.getLogger()

mcp = FastMCP("Brewfather MCP")

load_dotenv()

brewfather_client = BrewfatherInventoryClient()


@mcp.tool()
async def read_fermentables() -> str:
    try:
        data = await brewfather_client.get_fermentables_list()

        formatted_response = []
        for item in data.root:
            formatted = f"""
            Name: {item.name}
            Type: {item.type}
            Supplier: {item.supplier}
            Quantity: {item.inventory} kg
            Identifier: {item.id}
            """

            formatted_response.append(formatted)

        return "\n---\n".join(formatted_response)
    except Exception:
        logger.exception("Error happened")
        raise


@mcp.tool()
async def read_fermentable_detail(identifier: str) -> str:
    logger.info("received request")

    try:
        item = await brewfather_client.get_fermentable_detail(identifier)

        formatted_response = f"""
            Name: {item.name}
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


@mcp.tool()
async def read_hops() -> str:
    logger.info("received request")

    try:
        data = await brewfather_client.get_hops_list()

        formatted_response = []
        for item in data.root:
            formatted = f"""
            Identifier: {item.id}
            Alpha Acids (A.A): {item.alpha}
            Quantity: {item.inventory} grams
            Name: {item.name}
            Type: {item.type}
            Use: {item.use}
            """

            formatted_response.append(formatted)

        return "\n---\n".join(formatted_response)
    except Exception:
        logger.exception("Error happened")
        raise


@mcp.tool()
async def read_hops_detail(identifier: str) -> str:
    logger.info("received request")

    try:
        item = await brewfather_client.get_hop_detail(identifier)

        formatted = f"""
        Name: {item.name}
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


@mcp.tool()
async def read_yeasts() -> str:
    logger.info("received request")

    try:
        data = await brewfather_client.get_yeasts_list()

        formatted_response = []
        for item in data.root:
            formatted = f"""
            Identifier: {item.id}
            Attenuation (%): {item.attenuation}
            Quantity: {item.inventory} packets
            Name: {item.name}
            Type: {item.type}
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
        item = brewfather_client.get_yeast_detail(identifier)

        formatted = f"""
        Name: {item.name}
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


async def get_fermentables_summary() -> list[dict]:
    fermentables_data = await brewfather_client.get_fermentable_list()

    fermentables = []
    for f_data in fermentables_data:
        fermentable_data = brewfather_client.get_fermentable_detail(f_data.id)

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


async def get_hops_summary() -> dict:
    hops_data = await brewfather_client.get_hops_list()

    hops = []
    for h_data in hops_data:
        hop_data = await brewfather_client.get_hop_detail(h_data.id)

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


async def get_yeast_summary() -> dict:
    yeasts_data = await brewfather_client.get_yeasts_list()

    yeasts = []
    for y_data in yeasts_data:
        yeast_data = await brewfather_client.get_yeast_detail(y_data.id)

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
    except Exception:
        return dict(error=traceback.format_exc())
