# _*_ coding: utf_8 _*_

ALL = -1
NUM_ENTRIES = 25
"""
Entries per page.

This is the amount set in iRacing site. We shouldn't increase it.
"""

IRATING_OVAL_CHART = 1
IRATING_ROAD_CHART = 2

RACE_TYPE_OVAL = 1
RACE_TYPE_ROAD = 2

LIC_ROOKIE = 1
LIC_D = 2
LIC_C = 3
LIC_B = 4
LIC_A = 5
LIC_PRO = 6
LIC_PRO_WC = 7

SORT_IRATING = 'irating'
SORT_TIME = 'start_time'
SORT_POINTS = 'points'
ORDER_DESC = 'desc'
ORDER_ASC = 'asc'

# OTHER
EVENT_TEST = 1
EVENT_PRACTICE = 2
EVENT_QUALY = 3
EVENT_TTRIAL = 4
EVENT_RACE = 5
EVENT_OFFICIAL = 6
EVENT_UNOFFICIAL = 7

# INCIDENT FLAGS
# these are used in the laps data
FLAG_PITTED = 2
FLAG_OFF_TRACK = 4
FLAG_BLACK_FLAG = 8
FLAG_CAR_RESET = 16
FLAG_CONTACT = 32
FLAG_CAR_CONTACT = 64
FLAG_LOST_CONTROL = 128
FLAG_DISCONTINUITY = 256
FLAG_INTERPOLATED_CROSSING = 512
FLAG_CLOCK_SMASH = 1024
FLAG_TOW = 2048

INC_FLAGS = {
    0: "clean",
    2: "pitted",
    4: "off track",
    8: "black flag",
    16: "car reset",
    32: "contact",
    64: "car contact",
    128: "lost control",
    256: "discontinuity",
    512: "interpolated crossing",
    1024: "clock smash",
    2048: "tow"
}

# LOCATIONS
LOC_ALL = "null"
