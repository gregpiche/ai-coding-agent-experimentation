# Implements VehicleAgent: reactive agent that reads signal state and the cell ahead,
# returns a move-forward or stop decision for one vehicle.

from enum import Enum, auto
from typing import Any

from intersection.agents.base import Agent
from intersection.agents.traffic_light_agent import SignalPhase
from intersection.world.lane import Direction, LANE_LENGTH, STOP_LINE


class VehicleAction(Enum):
    """Decision returned by VehicleAgent.decide() each tick."""
    MOVE = auto()
    STOP = auto()


class VehicleAgent(Agent):
    """Reactive agent for a single vehicle.

    Holds only the vehicle's identifier; all simulation state is read from
    WorldState.  The engine is responsible for applying the returned
    VehicleAction to world state.
    """

    def __init__(self, vehicle_id: str) -> None:
        self.vehicle_id = vehicle_id

    def decide(self, world_state: "WorldState", vehicle=None) -> VehicleAction:
        """Return MOVE or STOP for this vehicle based on signal and space ahead."""
        if vehicle is None:
            vehicle = next(
                (v for v in world_state.vehicles if v.id == self.vehicle_id), None
            )
        if vehicle is None:
            return VehicleAction.STOP

        # Never enter an occupied cell
        if not self._space_ahead_free(vehicle, world_state.vehicles):
            return VehicleAction.STOP

        # Committed to crossing: always proceed toward exit (ignore signal)
        if vehicle.position >= STOP_LINE:
            return VehicleAction.MOVE

        # Green light: proceed through intersection
        if self._signal_allows(world_state.intersection.signal_phase, vehicle.direction):
            return VehicleAction.MOVE

        # Red/yellow: advance toward stop line but do not enter intersection
        if vehicle.position + 1 < STOP_LINE:
            return VehicleAction.MOVE

        return VehicleAction.STOP

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _signal_allows(phase: SignalPhase, direction: Direction) -> bool:
        """Return True only when the phase grants a full green for *direction*."""
        if direction in (Direction.NORTH, Direction.SOUTH):
            return phase == SignalPhase.NS_GREEN
        return phase == SignalPhase.EW_GREEN

    @staticmethod
    def _space_ahead_free(vehicle: Any, vehicles: list) -> bool:
        """Return True if no other vehicle occupies the cell directly ahead."""
        next_pos = vehicle.position + 1
        return not any(
            v.id != vehicle.id
            and v.direction == vehicle.direction
            and v.position == next_pos
            for v in vehicles
        )
