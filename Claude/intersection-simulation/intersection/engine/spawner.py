# Handles deterministic vehicle spawning: decides each tick whether a new vehicle should be added to each lane based on a configurable spawn rate and a seeded random source.

from __future__ import annotations

import random

from intersection.world.lane import Direction, Vehicle, LANE_LENGTH


class Spawner:
    def __init__(self, spawn_rate: float = 0.3, seed: int = 42) -> None:
        self._spawn_rate = spawn_rate
        self._rng = random.Random(seed)
        self._next_id = 0

    def spawn(self, world_state) -> list[Vehicle]:
        occupied_at_entry = {
            v.direction for v in world_state.vehicles if v.position == 0
        }
        new_vehicles: list[Vehicle] = []
        for direction in Direction:
            if self._rng.random() < self._spawn_rate and direction not in occupied_at_entry:
                vehicle = Vehicle(id=f"v{self._next_id}", direction=direction, position=0)
                self._next_id += 1
                new_vehicles.append(vehicle)
        return new_vehicles
