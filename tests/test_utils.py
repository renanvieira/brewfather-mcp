import asyncio
from typing import Any, Coroutine
from unittest.mock import AsyncMock

import pytest
from brewfather_mcp.utils import get_in_batches
from pydantic import BaseModel, RootModel


# Mock the models that would be used
class InventoryItem(BaseModel):
    id: str
    name: str = ""


@pytest.mark.asyncio
async def test_get_in_batches_empty_list():
    """Test function with an empty list."""
    mock_async_fn = AsyncMock()
    empty_list = RootModel[list[InventoryItem]](root=[])

    result = await get_in_batches(10, mock_async_fn, empty_list)

    assert result == []
    mock_async_fn.assert_not_called()


@pytest.mark.asyncio
async def test_get_in_batches_single_batch():
    """Test function with items that fit within a single batch."""
    batch_size = 5
    items = [InventoryItem(id=f"id_{i}") for i in range(3)]
    main_iterable = RootModel[list[InventoryItem]](root=items)

    async def mock_getter(item_id: str) -> InventoryItem:
        return InventoryItem(id=item_id, name=f"Item {item_id}")

    result = await get_in_batches(batch_size, mock_getter, main_iterable)

    assert len(result) == 3
    assert all(isinstance(item, InventoryItem) for item in result)
    assert [item.id for item in result] == ["id_0", "id_1", "id_2"]
    assert [item.name for item in result] == ["Item id_0", "Item id_1", "Item id_2"]


@pytest.mark.asyncio
async def test_get_in_batches_multiple_batches():
    """Test function with items that require multiple batches."""
    batch_size = 2
    items = [InventoryItem(id=f"id_{i}") for i in range(5)]
    main_iterable = RootModel[list[InventoryItem]](root=items)

    call_order = []

    async def mock_getter(item_id: str) -> InventoryItem:
        # Track the order of calls
        call_order.append(item_id)
        # Simulate different processing times
        await asyncio.sleep(0.01 if item_id == "id_2" else 0.001)
        return InventoryItem(id=item_id, name=f"Item {item_id}")

    # Act
    result = await get_in_batches(batch_size, mock_getter, main_iterable)

    # Assert
    assert len(result) == 5
    # Verify all items are processed
    assert sorted([item.id for item in result]) == [
        "id_0",
        "id_1",
        "id_2",
        "id_3",
        "id_4",
    ]
    # Verify items are processed in batches
    assert len(call_order) == 5


@pytest.mark.asyncio
async def test_get_in_batches_exact_batch_size():
    """Test function with items that exactly match the batch size."""
    batch_size = 3
    items = [InventoryItem(id=f"id_{i}") for i in range(6)]
    main_iterable = RootModel[list[InventoryItem]](root=items)

    processed_batches = []
    currently_processing = set()

    async def mock_getter(item_id: str) -> InventoryItem:
        # Add to currently processing set
        currently_processing.add(item_id)
        # Small delay to ensure concurrent execution within a batch
        await asyncio.sleep(0.05)
        # Record the batch before removing from processing
        if len(currently_processing) == batch_size:
            processed_batches.append(set(currently_processing))
        currently_processing.remove(item_id)
        return InventoryItem(id=item_id, name=f"Processed {item_id}")

    result = await get_in_batches(batch_size, mock_getter, main_iterable)

    assert len(result) == 6
    assert sorted([item.id for item in result]) == [
        "id_0",
        "id_1",
        "id_2",
        "id_3",
        "id_4",
        "id_5",
    ]
    # We should have had 2 full batches with batch_size items
    assert len(processed_batches) == 2


@pytest.mark.asyncio
async def test_get_in_batches_error_handling():
    """Test how the function handles errors in the async function."""
    batch_size = 3
    items = [InventoryItem(id=f"id_{i}") for i in range(5)]
    main_iterable = RootModel[list[InventoryItem]](root=items)

    async def mock_getter(item_id: str) -> InventoryItem:
        if item_id == "id_2":
            raise ValueError("Error processing id_2")
        return InventoryItem(id=item_id, name=f"Item {item_id}")

    with pytest.raises(ValueError, match="Error processing id_2"):
        await get_in_batches(batch_size, mock_getter, main_iterable)


@pytest.mark.asyncio
async def test_get_in_batches_preserves_order():
    """Test that the function preserves the order of results based on input order."""
    batch_size = 2
    items = [
        InventoryItem(id="id_C"),
        InventoryItem(id="id_A"),
        InventoryItem(id="id_D"),
        InventoryItem(id="id_B"),
    ]
    main_iterable = RootModel[list[InventoryItem]](root=items)

    async def mock_getter(item_id: str) -> InventoryItem:
        # Simulate varying processing times
        delay = 0.02 if item_id in ["id_A", "id_D"] else 0.01
        await asyncio.sleep(delay)
        return InventoryItem(id=item_id, name=f"Item {item_id}")

    result = await get_in_batches(batch_size, mock_getter, main_iterable)

    # The order of results should match the order of tasks, which is based on the input order
    assert [item.id for item in result] == ["id_C", "id_A", "id_D", "id_B"]
