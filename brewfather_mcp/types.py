from enum import auto
import urllib.parse
from enum import StrEnum
from pydantic import BaseModel, Field, RootModel, field_validator
from datetime import datetime

from pydantic.config import ConfigDict
import brewfather_mcp.utils as utils


class InventoryCategory(StrEnum):
    FERMENTABLES = auto()
    HOPS = auto()
    MISCELLANEOUS = "miscs"
    YEASTS = auto()


class Fermentable(BaseModel):
    """
    Represents a fermentable ingredient like malt or adjunct.
    """

    id: str = Field(alias="_id")
    attenuation: float | None = None
    inventory: float
    name: str
    supplier: str
    type: str

    model_config = {
        "populate_by_name": True,
    }


class FermentableList(RootModel):
    root: list[Fermentable]


class Timestamp(BaseModel):
    """Represents a timestamp with seconds and nanoseconds."""

    seconds: int = Field(alias="_seconds")
    nanoseconds: int = Field(alias="_nanoseconds")

    def to_datetime(self) -> datetime:
        """Convert the timestamp to a Python datetime object."""
        return datetime.fromtimestamp(self.seconds + (self.nanoseconds / 1e9))


class FermentableDetail(Fermentable):
    """
    Comprehensive model for a brewing ingredient with detailed properties.
    """

    protein: float | None = None
    diastatic_power: float | None = Field(alias="diastaticPower", default=None)
    not_fermentable: bool = Field(alias="notFermentable")
    substitutes: str = ""
    potential: float
    timestamp_ms: int = Field(alias="_timestamp_ms")
    percentage: float = 0
    grain_category: str | None = Field(alias="grainCategory", default=None)
    created: Timestamp = Field(alias="_created")
    user_notes: str | None = Field(alias="userNotes", default=None)
    max_in_batch: float | None = Field(alias="maxInBatch", default=None)
    fgdb: float | None = None
    version: str = Field(alias="_version")
    acid: float | None = None
    cgdb: float | None = None
    best_before_date: str | None = Field(alias="bestBeforeDate", default=None)
    hidden: bool = False
    amount: float | None = False
    origin: str | None = None
    cost_per_amount: float | None = Field(alias="costPerAmount", default=None)
    manufacturing_date: str | None = Field(alias="manufacturingDate", default=None)
    lot_number: str | None = Field(alias="lotNumber", default=None)
    notes: str | None = None
    ibu_per_amount: float | None = Field(alias="ibuPerAmount", default=None)
    friability: float | None = None
    rev: str = Field(alias="_rev")
    excluded: bool = False
    timestamp: Timestamp = Field(alias="_timestamp")
    color: float = 0
    potential_percentage: float = Field(alias="potentialPercentage", default=0)
    moisture: float | None = None
    fan: float | None = None
    coarse_fine_diff: float | None = Field(alias="coarseFineDiff", default=None)
    used_in: str = Field(alias="usedIn", default="")

    model_config = {
        "populate_by_name": True,
    }

    @field_validator("manufacturing_date", "best_before_date", mode="before")
    @classmethod
    def convert_timestamp_to_isodate(cls, value):
        return utils.convert_timestamp_to_iso8601(value)


class Hop(BaseModel):
    """
    Base model for hop information with essential properties.
    """

    id: str = Field(alias="_id")
    alpha: float
    inventory: float
    name: str
    type: str
    use: str

    model_config = {
        "populate_by_name": True,
    }


class HopList(RootModel):
    """
    A collection of hops.
    """

    root: list[Hop]


class HopDetail(Hop):
    """
    Extended hop model with all additional properties.
    """

    farnesene: float | None = None
    notes: str = ""
    hidden: bool = False
    caryophyllene: float | None = None
    year: int | None = None
    usage: str | None = None
    origin: str | None = None
    rev: str = Field(alias="_rev")
    oil: float | None = None
    timestamp: Timestamp = Field(alias="_timestamp")
    version: str = Field(alias="_version")
    beta: float | None = None
    amount: float | None = None
    temp: float | None = None
    substitutes: str = ""
    best_before_date: str | None = Field(
        alias="bestBeforeDate", default=None
    )  # Unix timestamp in milliseconds
    used_in: str = Field(alias="usedIn", default="")
    myrcene: float | None = None
    timestamp_ms: int = Field(alias="_timestamp_ms")
    cohumulone: float | None = None
    humulene: float | None = None
    created: Timestamp = Field(alias="_created")
    manufacturing_date: str | None = Field(
        alias="manufacturingDate", default=None
    )  # Unix timestamp in milliseconds
    time: int | None = None
    user_notes: str = Field(alias="userNotes", default="")
    ibu: float = 0
    hsi: float | None = None  # Hop Storage Index

    model_config = {
        "populate_by_name": True,
    }

    @field_validator("manufacturing_date", "best_before_date", mode="before")
    @classmethod
    def convert_timestamp_to_isodate(cls, value):
        return utils.convert_timestamp_to_iso8601(value)


class Yeast(BaseModel):
    """Basic yeast model with essential properties."""

    id: str = Field(alias="_id")
    attenuation: int
    inventory: float  # Using float to handle both integer and decimal values
    name: str
    type: str

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "_id": "default-016efc",
                    "attenuation": 81,
                    "inventory": 0,
                    "name": "Safale American",
                    "type": "Ale",
                }
            ]
        },
    }


class YeastList(RootModel):
    """A collection of yeasts."""

    root: list[Yeast]


class YeastDetail(Yeast):
    """Extended yeast model with all additional properties."""

    laboratory: str
    min_attenuation: int | None = Field(alias="minAttenuation", default=None)
    max_abv: int | None = Field(alias="maxAbv", default=None)
    hidden: bool = False
    min_temp: int | None = Field(alias="minTemp", default=None)
    max_temp: int | None = Field(alias="maxTemp", default=None)
    product_id: str | None = Field(alias="productId", default=None)
    age_rate: int | None = Field(alias="ageRate", default=None)
    description: str | None = None
    max_attenuation: int | None = Field(alias="maxAttenuation", default=None)
    cells_per_pkg: int | None = Field(alias="cellsPerPkg", default=None)
    form: str | None = None
    flocculation: str | None = None
    unit: str | None = None
    best_before_date: int | None = Field(alias="bestBeforeDate", default=None)
    amount: float | None = None
    ferments_all: bool = Field(alias="fermentsAll", default=False)
    manufacturing_date: str | None = Field(alias="manufacturingDate", default=None)
    timestamp: Timestamp = Field(alias="_timestamp")
    timestamp_ms: int = Field(alias="_timestamp_ms")
    user_notes: str = Field(alias="userNotes", default="")
    rev: str = Field(alias="_rev")
    created: Timestamp = Field(alias="_created")
    version: str = Field(alias="_version")

    @field_validator("manufacturing_date", "best_before_date", mode="before")
    @classmethod
    def convert_timestamp_to_isodate(cls, value):
        return utils.convert_timestamp_to_iso8601(value)

    model_config = {
        "populate_by_name": True,
    }


class OrderByDirection(StrEnum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class ListQueryParams:
    inventory_negative: bool | None = None
    complete: bool | None = None
    inventory_exists: bool | None = None
    limit: int | None = None
    start_after: str | None = None
    order_by: str | None = None
    order_by_direction: OrderByDirection | None = None

    def as_query_param_str(self) -> str | None:
        qs = ""

        if self.inventory_negative:
            qs += f"inventory_negative={self.inventory_negative}"

        if self.complete:
            qs += f"complete={self.complete}"
        if self.inventory_exists:
            qs += f"inventory_exists={self.inventory_exists}"

        if self.limit:
            qs += f"limit={self.limit}"

        if self.start_after:
            qs += f"start_after={urllib.parse.quote_plus(self.start_after)}"

        if self.order_by:
            qs += f"order_by={urllib.parse.quote_plus(self.order_by)}"

        if self.order_by_direction:
           qs += f"order_by_direction={self.order_by_direction}"

        if qs:
            return qs
        else:
            None
