from enum import Enum


__all__ = [
    "Category",
    "License",
    "TimeOfDay",
]


class Category(Enum):
    oval = 1
    road = 2
    dirt_oval = 3
    dirt_road = 4


class License(Enum):
    R = 1
    D = 2
    C = 3
    B = 4
    A = 5
    PRO = 6
    PRO_WORLD_CUP = 7


class TimeOfDay(Enum):
    afternoon = 0
    morning = 1
    late_afternoon = 2
    night = 3
    specific_time = 4
    sunrise = 5
    # unknown = 6
    # unknown = 7
    sunset = 8
    noon = 9
