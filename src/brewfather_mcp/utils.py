import asyncio
from collections.abc import Coroutine
import typing
from datetime import datetime
from itertools import batched

from pydantic import RootModel

if typing.TYPE_CHECKING:
    from brewfather_mcp.types import (
        InventoryItem,
    )

AnyDict = dict[str, str | int | float | None]
AnyDictList = list[AnyDict]


def convert_timestamp_to_iso8601(value: int | None):
    """Convert Unix timestamp to ISO 8601 formatted string."""
    if value is None:
        return None

    # If the value is an integer (Unix timestamp), convert it
    if value:
        # Check if it's in milliseconds (13 digits) or seconds (10 digits)
        if len(str(value)) > 10:  # milliseconds
            timestamp_seconds = value / 1000
        else:  # seconds
            timestamp_seconds = value

        dt = datetime.fromtimestamp(timestamp_seconds)
        return dt.isoformat()

    return value


async def get_in_batches[TReturn: "InventoryItem", TIterable: "InventoryItem"](
    batch_size: int,
    async_fn: typing.Callable[[str], Coroutine[typing.Any, typing.Any, TReturn]],
    main_iterable: RootModel[list[TIterable]],
) -> list[TReturn]:
    """Auxiliary function to execute function in async batches."""
    detail_results: list[TReturn] = []
    detail_tasks = [async_fn(data.id) for data in main_iterable.root]
    batches = batched(detail_tasks, batch_size)
    for batch in batches:
        detail_results.extend(await asyncio.gather(*batch))

    return detail_results
