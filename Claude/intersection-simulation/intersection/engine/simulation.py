# Defines SimulationEngine: the main tick loop that sequences spawning, agent updates, movement resolution, exit removal, and tick advancement.

from __future__ import annotations

from intersection.agents.traffic_light_agent import PHASE_DURATIONS
from intersection.agents.vehicle_agent import VehicleAgent
from intersection.engine.resolver import resolve_movements
from intersection.world.lane import LANE_EXIT, LANE_LENGTH


class SimulationEngine:
    def __init__(self, world_state, traffic_light_agent, spawner) -> None:
        self._world = world_state
        self._traffic_light = traffic_light_agent
        self._spawner = spawner
        self._vehicle_agents: dict[str, VehicleAgent] = {}

    def tick(self) -> None:
        world = self._world

        # 1. Spawn new vehicles
        new_vehicles = self._spawner.spawn(world)
        for v in new_vehicles:
            world.vehicles.append(v)
            self._vehicle_agents[v.id] = VehicleAgent(v.id)

        # 2. Decrement phase timer (floor at 0), then ask traffic light to decide
        world.intersection.phase_timer = max(0, world.intersection.phase_timer - 1)
        next_phase = self._traffic_light.decide(world)
        if next_phase is not None:
            world.intersection.signal_phase = next_phase
            world.intersection.phase_timer = PHASE_DURATIONS[next_phase]

        # 3. Collect vehicle decisions
        decisions = {
            v.id: self._vehicle_agents[v.id].decide(world, v)
            for v in world.vehicles
        }

        # 4. Resolve movements
        resolve_movements(world, decisions)

        # 5. Remove exited vehicles (single pass)
        remaining, exited_ids = [], []
        for v in world.vehicles:
            if v.position >= LANE_EXIT:
                exited_ids.append(v.id)
            else:
                remaining.append(v)
        world.vehicles = remaining
        for vid in exited_ids:
            del self._vehicle_agents[vid]

        # 6. Advance tick
        world.tick += 1

    def run(self, ticks: int):
        for _ in range(ticks):
            self.tick()
        return self._world
