# Defines the abstract Agent base class with a single decide() interface that all agents must implement.

from abc import ABC, abstractmethod
from typing import Any


class Agent(ABC):
    """Abstract base for all simulation agents.

    Agents are read-only consumers of WorldState: they inspect the world
    and return a decision each tick, but never mutate state directly.
    """

    @abstractmethod
    def decide(self, world_state: "WorldState") -> Any:
        """Inspect *world_state* and return a decision for this tick.

        Concrete agents must override this method.  The return type varies
        by agent: TrafficLightAgent returns a phase transition, VehicleAgent
        returns a movement action.  The engine is responsible for applying
        the returned decision to world state.
        """
