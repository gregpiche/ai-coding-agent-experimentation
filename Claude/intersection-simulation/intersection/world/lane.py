# Defines Lane and Direction: a directed queue of vehicle positions along one of the four approach roads (north, south, east, west).

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

LANE_LENGTH = 10  # intersection center reference; intersection occupies positions 9–11
LANE_EXIT = 21    # full grid size; vehicle exits when position >= this
STOP_LINE = LANE_LENGTH - 1  # position 9: first intersection cell; vehicles at or past this are committed


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


@dataclass
class Vehicle:
    id: str
    direction: Direction
    position: int  # 0 = entry, increases toward exit


@dataclass
class Lane:
    direction: Direction
