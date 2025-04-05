import asyncio
import typing
from datetime import datetime
from itertools import batched

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


async def get_in_batches(
    n: int,
    main_iterable: list[typing.Any],
    callable: typing.Callable[[str], typing.Any],  # type: ignore
) -> list[typing.Any]:  # noqa
    detail_results = []
    detail_tasks = [callable(data.id) for data in main_iterable]
    batches = batched(detail_tasks, n)
    for batch in batches:
        detail_results.extend(await asyncio.gather(*batch))

    return detail_results
