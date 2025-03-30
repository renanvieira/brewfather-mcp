from enum import auto
from enum import StrEnum
from pydantic import BaseModel, Field, RootModel
from datetime import datetime


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
        "json_schema_extra": {
            "examples": [
                {
                    "_id": "default-03044fe",
                    "attenuation": 0,
                    "inventory": 0.7,
                    "name": "Rice Hulls",
                    "supplier": "Briess",
                    "type": "Adjunct",
                }
            ]
        },
    }


class FermentableList(RootModel):
    root: list[Fermentable]


class Timestamp(BaseModel):
    """Represents a timestamp with seconds and nanoseconds."""

    _seconds: int
    _nanoseconds: int

    def to_datetime(self) -> datetime:
        """Convert the timestamp to a Python datetime object."""
        return datetime.fromtimestamp(self._seconds + (self._nanoseconds / 1e9))


class FermentableDetail(Fermentable):
    """
    Comprehensive model for a brewing ingredient with detailed properties.
    """

    protein: float | None = None
    diastaticPower: float | None = None
    notFermentable: bool
    substitutes: str = ""
    potential: float
    _timestamp_ms: int
    percentage: float = 0
    grainCategory: str | None = None
    _created: Timestamp
    userNotes: str | None = None
    maxInBatch: float | None = None
    fgdb: float | None = None
    _version: str
    acid: float | None = None
    cgdb: float | None = None
    bestBeforeDate: str | None = None
    hidden: bool = False
    amount: float
    origin: str | None = None
    costPerAmount: float | None = None
    manufacturingDate: str | None = None
    lotNumber: str | None = None
    notes: str | None = None
    ibuPerAmount: float | None = None
    friability: float | None = None
    _rev: str
    excluded: bool = False
    _timestamp: Timestamp
    color: float = 0
    potentialPercentage: float = 0
    moisture: float | None = None
    fan: float | None = None
    coarseFineDiff: float | None = None
    usedIn: str = ""

    model_config = {
        "populate_by_name": True,
    }


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
    _rev: str
    oil: float | None = None
    _timestamp: Timestamp
    _version: str
    beta: float | None = None
    amount: float | None = None
    temp: float | None = None
    substitutes: str = ""
    bestBeforeDate: int | None = None  # Unix timestamp in milliseconds
    usedIn: str = ""
    myrcene: float | None = None
    _timestamp_ms: int
    cohumulone: float | None = None
    humulene: float | None = None
    _created: Timestamp
    manufacturingDate: int | None = None  # Unix timestamp in milliseconds
    time: int | None = None
    userNotes: str = ""
    ibu: float = 0
    hsi: float | None = None  # Hop Storage Index

    model_config = {
        "populate_by_name": True,
    }


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
    minAttenuation: int | None = None
    maxAbv: int | None = None
    hidden: bool = False
    minTemp: int | None = None
    maxTemp: int | None = None
    productId: str | None = None
    ageRate: int | None = None
    description: str | None = None
    maxAttenuation: int | None = None
    cellsPerPkg: int | None = None
    form: str | None = None
    flocculation: str | None = None
    unit: str | None = None
    bestBeforeDate: int | None = None
    amount: float | None = None
    fermentsAll: bool = False
    manufacturingDate: int | None = None
    _timestamp: Timestamp
    _timestamp_ms: int
    userNotes: str = ""
    _rev: str
    _created: Timestamp
    _version: str

    model_config = {
        "populate_by_name": True,
    }
