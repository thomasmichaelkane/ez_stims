"""
Enums:
------
- Behavior: An enumeration of stimulus behavior modes, BOUNCE or LOOP.
- StimType: An enumeration of stimulus types, CHECK or BAR.
"""
from enum import Enum

class Behavior(Enum):
    BOUNCE = 1
    LOOP = 2
    
class StimType(Enum):
    CHECK = 1
    BAR = 2