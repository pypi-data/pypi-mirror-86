from dataclasses import dataclass, field
from paddock._dataclasses import require_kwargs_on_init
from paddock._marshmallow import (
    JsonModelBaseclass,
    QuotedStringField,
)


__all__ = [
    "CarRecord",
]


@dataclass
class CarRecord(JsonModelBaseclass):
    id: int = field(metadata={"data_key": "carid"})
    """
    Unique identifier for the car.
    """

    name: str = field(metadata={
        "marshmallow_field": QuotedStringField(data_key="car_name")
    })
    """
    Human-readable car name.
    """


require_kwargs_on_init(CarRecord)
