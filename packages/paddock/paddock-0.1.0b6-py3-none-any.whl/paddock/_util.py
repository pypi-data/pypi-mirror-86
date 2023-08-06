from typing import (
    Optional,
    Type,
    TypeVar,
)

__all__ = [
    "format_results",
    "maybe_value_of",
]

T = TypeVar("T")


def format_results(results, header):
    newres = []
    for row in results:
        newr = {}
        for k, v in row.items():
            newr[header[k]] = v
        newres.append(newr)
    return newres


def maybe_value_of(enum_type: Type[T], value: int) -> Optional[T]:
    try:
        return enum_type(value)
    except ValueError:
        return None
