import datetime as dt
import typing

import marshmallow as m
from enum import Enum
from marshmallow_dataclass import class_schema
from typing import (
    Any,
    Optional,
    Type,
    TypeVar,
)
from urllib.parse import quote_plus, unquote_plus


__all__ = [
    "JsonModelMetaclass",
    "JsonModelBaseclass",
    "QuotedStringField",
    "NumericBooleanField",
    "UtcMillisecondDateTime",
]


T = TypeVar("T")


class JsonModelMetaclass(type):

    # noinspection PyPep8Naming
    @property
    def Schema(cls) -> Type[m.Schema]:
        return class_schema(cls)


class JsonModelBaseclass(metaclass=JsonModelMetaclass):
    class Meta:
        unknown = m.EXCLUDE


# noinspection DuplicatedCode
class QuotedStringField(m.fields.Field):

    def __init__(
            self,
            deserialize_empty_as_none: bool = False,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.deserialize_empty_as_none = deserialize_empty_as_none

    def _serialize(self, value, attr, obj, **kwargs) -> Optional[str]:
        if value is None:
            return None
        else:
            return quote_plus(value)

    def _deserialize(self, value, attr, data, **kwargs) -> Optional[str]:
        if value is None:
            return None
        elif self.deserialize_empty_as_none and len(value) == 0:
            return None
        else:
            return unquote_plus(value)


# noinspection DuplicatedCode
class NumericBooleanField(m.fields.Field):

    def _serialize(self, value, attr, obj, **kwargs) -> Optional[int]:
        if value is None:
            return None
        else:
            return 1 if value else 0

    def _deserialize(self, value, attr, data, **kwargs) -> Optional[bool]:
        if value is None:
            return None
        elif value == 0:
            return False
        elif value == 1:
            return True
        else:
            raise ValueError(f"Expected 0, 1, or None, found: {value}")


# noinspection DuplicatedCode
class UtcMillisecondDateTime(m.fields.Field):

    def _serialize(
            self, value: dt.datetime, attr, obj, **kwargs
    ) -> Optional[int]:
        if value is None:
            return None
        else:
            return int(value.timestamp() * 1_000)

    def _deserialize(
            self, value, attr, data, **kwargs
    ) -> Optional[dt.datetime]:
        if value is None:
            return None
        else:
            return dt.datetime.utcfromtimestamp(value / 1_000)
