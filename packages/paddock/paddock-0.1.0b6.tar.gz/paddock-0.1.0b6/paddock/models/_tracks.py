from dataclasses import dataclass, field
from typing import Optional
from paddock.models._common import Category
from paddock._dataclasses import require_kwargs_on_init
from paddock._marshmallow import (
    JsonModelBaseclass,
    QuotedStringField,
    NumericBooleanField,
)
from paddock._util import maybe_value_of


__all__ = [
    "TrackConfigurationRecord",
]


@dataclass
class TrackConfigurationRecord(JsonModelBaseclass):
    id: int = field(metadata={"data_key": "trackid"})
    """
    iRacing's unique circuit identifier.
    """

    name: str = field(metadata={
        "marshmallow_field": QuotedStringField(data_key="track_name")
    })
    """
    Name of the track.
    """

    configuration_name: Optional[str] = field(metadata={
        "marshmallow_field": QuotedStringField(
            data_key="config_name",
            deserialize_empty_as_none=True,
        )
    })
    """
    Name of the configuration.
    """

    configuration_order: int = field(metadata={"data_key": "priority"})
    """
    This field is used by the interface to influence the order of the track
    configurations in the drop-down or other list.
    """

    grid_stalls: int = field(metadata={"data_key": "ngridstalls"})
    """
    Number of stalls on the grid before the start/finish line.
    """

    pit_stalls: int = field(metadata={"data_key": "npitstalls"})
    """
    Number of spaces in the pit lane.
    """

    max_cars_on_track: int = field(metadata={"data_key": "maxcarsontrack"})
    """
    Maximum number of cars that can be in a session.
    """

    short_parade_lap: bool = field(metadata={
        "data_key": "hasShortParadeLap"
    })
    """
    Whether a shortened formation / pace / parade lap is configurable.
    """

    is_fully_lit: bool = field(metadata={"data_key": "fullylit"})
    """
    Whether circuit has track lighting / is visible at all times of day.
    """

    is_dirt: bool = field(metadata={
        "marshmallow_field": NumericBooleanField(data_key="isdirt")
    })
    "Whether circuit is a dirt track or not."

    is_oval: bool = field(metadata={
        "marshmallow_field": NumericBooleanField(data_key="isoval")
    })
    """
    Whether circuit is considered an oval or not.
    """

    latitude: float
    """
    Latitude of circut's location on the globe.
    """

    longitude: float
    """
    Longitude of circut's location on the globe.
    """

    coordinates: str = field(metadata={
        "marshmallow_field": QuotedStringField(data_key="coordinates")
    })
    """
    Latitude and longitude string formatted for presentation on a
    user interface.
    """

    time_zone: str = field(metadata={
        "marshmallow_field": QuotedStringField(data_key="timeZoneId")
    })
    """
    A standard, ICANN tzdata formatted timezone.
    """

    is_lap_scoring: bool = field(metadata={
        "marshmallow_field": NumericBooleanField(data_key="lapscoring")
    })
    """
    Only tracks that do not have a full circuit lap like Nurburgring
    Touristenfahrten have this set to True.
    """

    raw_category: int = field(metadata={
        "data_key": "catid"
    })
    """
    Category of racing. This is the raw value the iRacing API sends.

    Consider using category property instead.
    """

    category: Optional[Category] = field(init=False)
    """
    raw_category coerced into an easy-to-read enum if a recognizable value
    """

    is_road: bool = field(init=False)
    """
    Whether the track is a road course.
    """

    is_paved: bool = field(init=False)
    """
    Whether the track is paved (not dirt).
    """

    def __post_init__(self):
        self.category = maybe_value_of(Category, self.raw_category)
        self.is_road = not self.is_oval
        self.is_paved = not self.is_dirt


require_kwargs_on_init(TrackConfigurationRecord)
