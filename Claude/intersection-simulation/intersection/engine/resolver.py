# Applies vehicle decisions to world state and enforces collision avoidance: ensures no two vehicles occupy the same cell after movement is resolved.

from __future__ import annotations

from intersection.world.lane import Direction
from intersection.agents.vehicle_agent import VehicleAction


def resolve_movements(world_state, decisions: dict[str, VehicleAction]) -> None:
    """Apply movement decisions to world state with collision avoidance.

    Processes vehicles front-to-back (highest position first) within each
    direction to prevent chained blocking.
    """
    # Group vehicles by direction
    by_direction: dict[Direction, list] = {d: [] for d in Direction}
    for vehicle in world_state.vehicles:
        by_direction[vehicle.direction].append(vehicle)

    for direction, group in by_direction.items():
        # Sort front-to-back: highest position first
        group.sort(key=lambda v: v.position, reverse=True)

        # Build occupied set for this direction
        occupied: set[int] = {v.position for v in group}

        for vehicle in group:
            if decisions.get(vehicle.id) == VehicleAction.MOVE:
                next_pos = vehicle.position + 1
                if next_pos not in occupied:
                    occupied.discard(vehicle.position)
                    vehicle.position = next_pos
                    occupied.add(next_pos)
