import datetime as dt
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Optional,
    List,
)
from paddock.models._common import (
    Category,
    License,
    TimeOfDay,
)
from paddock._dataclasses import require_kwargs_on_init
from paddock._marshmallow import (
    JsonModelBaseclass,
    QuotedStringField,
    UtcMillisecondDateTime,
)
from paddock._util import maybe_value_of


__all__ = [
    "Season",
    "SeasonCar",
    "SeasonTrack",
]


# TODO: Car class.


@dataclass
class SeasonCar(JsonModelBaseclass):
    id: int = field(metadata={"data_key": "id"})
    """
    Unique identifier for the car.
    """

    name: str = field(metadata={
        "marshmallow_field": QuotedStringField(data_key="name")
    })
    """
    Human-readable car name.
    """


@dataclass
class SeasonTrack(JsonModelBaseclass):
    id: int = field(metadata={"data_key": "id"})
    """
    Unique identifier for the track + configuration combination.
    """

    name: str = field(metadata={
        "marshmallow_field": QuotedStringField(data_key="name")
    })
    """
    Human-readable track name.
    """

    configuration_name: Optional[str] = field(metadata={
        "marshmallow_field": QuotedStringField(
            data_key="config",
            deserialize_empty_as_none=True
        )
    })
    """
    Human readable track configuration name.
    """

    race_week: int = field(metadata={"data_key": "raceweek"})
    """
    Race week is 1-indexed, with the first race week being week 1.

    In a normal 12-week series, the range of values is 1..12, inclusive
    on both ends.
    """

    raw_time_of_day: int = field(metadata={"data_key": "timeOfDay"})
    """
    Time of day that the race will take place. This is the raw value. Consider
    using the time_of_day property instead.
    """

    time_of_day: Optional[int] = field(init=False)
    """
    raw_time_of_day coerced into an easy-to-read enum if a recognizable value
    """

    def __post_init__(self):
        self.time_of_day = maybe_value_of(TimeOfDay, self.raw_time_of_day)


@dataclass
class Season(JsonModelBaseclass):
    series_id: int = field(metadata={"data_key": "seriesid"})
    """
    Unique identifier for the series.

    Series are repeated across multiple seasons.
    """

    season_id: int = field(metadata={"data_key": "seasonid"})
    """
    Unique identifier for this particular season of this series.

    Two different series will never have the same season ID. Likewise,
    the same series may be present in a list, but never the same season of
    the series.
    """

    year: int = field(metadata={"data_key": "year"})
    """
    4-digit year. E.g., 2020.
    """

    quarter: int = field(metadata={"data_key": "quarter"})
    """
    Quarter of the year. Legal values: 1, 2, 3, 4.
    """

    race_week: int = field(metadata={"data_key": "raceweek"})
    """
    Race week is 0-indexed, with the first race week being week 0.
    
    IMPORTANT: This value is different from season race week, which is
               1-indexed. Probably it's because this field is only used for
               sorting, where the season race week is used for user interfaces.
    
    In a normal 12-week series, the range of values is 0..11, inclusive
    on both ends. It's literally the index of the track in the tracks list.
    """

    series_name: str = field(metadata={
        "marshmallow_field": QuotedStringField(data_key="seriesshortname")
    })
    """
    Human-readable name for the series.
    """

    starts_at: dt.datetime = field(metadata={
        "marshmallow_field": UtcMillisecondDateTime(data_key="start"),
    })
    """
    Time when the series starts, in UTC.
    """

    ends_at: dt.datetime = field(metadata={
        "marshmallow_field": UtcMillisecondDateTime(data_key="end"),
    })
    """
    Time when the series ends, in UTC.
    """

    is_active: bool = field(metadata={"data_key": "active"})
    """
    Whether or not this season is currently between the start and end times.
    """

    is_lite: bool = field(metadata={"data_key": "islite"})
    """
    It is unknown what this field means. No seasons are currently reporting
    True at the time this code was written.
    """

    raw_license: int = field(metadata={"data_key": "serieslicgroupid"})
    """
    Raw license integer value stored by iRacing servers.

    Consider using license instead..
    """

    raw_category: int = field(metadata={"data_key": "catid"})
    """
    Raw category integer value stored by iRacing servers.

    Consider using category instead..
    """

    category: Optional[Category] = field(init=False)
    """
    Friendly category (e.g., road).

    None if raw_category is not able to be mapped to a Category.
    """

    license: Optional[License] = field(init=False)
    """
    Friendly license (e.g., A).

    None if raw_license is not able to be mapped to a License.
    """

    tracks: List[SeasonTrack]
    """
    List of tracks in this season of this series.
    """

    cars: List[SeasonCar]
    """
    List of cars allowable in this season of this series.
    """

    def __post_init__(self):
        self.license = maybe_value_of(License, self.raw_license)
        self.category = maybe_value_of(Category, self.raw_category)


require_kwargs_on_init(Season)
require_kwargs_on_init(SeasonTrack)
