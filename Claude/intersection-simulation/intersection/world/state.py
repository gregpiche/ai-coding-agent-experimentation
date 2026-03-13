# Defines WorldState: the snapshot of the full simulation at a single tick, including tick counter, vehicle list, intersection signal state, and lane queues.

from __future__ import annotations

from dataclasses import dataclass, field

from intersection.world.lane import Direction, Lane, Vehicle
from intersection.world.intersection import IntersectionState


@dataclass
class WorldState:
    tick: int
    vehicles: list[Vehicle]
    intersection: IntersectionState
    lanes: dict[Direction, Lane]
