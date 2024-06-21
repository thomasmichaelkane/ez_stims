"""
Enums:
------
- EdgeBehavior: An enumeration of kalatsky stimulus behavior modes, BOUNCE or LOOP.
- GratBehavior: An enumeration of grating stimulus behavior modes, DRIFT or FLICKER.
- StimType: An enumeration of stimulus types, CHECK or BAR.
"""
from enum import Enum

class EdgeBehavior(Enum):
    BOUNCE = 1
    LOOP = 2

class GratBehavior(Enum):
    DRIFT = 1
    FLICKER = 2

class StimType(Enum):
    CHECK = 1
    BAR = 2