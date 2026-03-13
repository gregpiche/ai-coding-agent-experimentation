# Implements TrafficLightAgent: reads the current signal phase and timer,
# returns the next phase transition when the timer expires on a fixed cycle.

from __future__ import annotations

from enum import Enum, auto
from typing import Optional

from intersection.agents.base import Agent


class SignalPhase(Enum):
    """Four phases of the fixed traffic light cycle."""
    NS_GREEN  = auto()
    NS_YELLOW = auto()
    EW_GREEN  = auto()
    EW_YELLOW = auto()


# Tick duration for each phase.
PHASE_DURATIONS: dict[SignalPhase, int] = {
    SignalPhase.NS_GREEN:  20,
    SignalPhase.NS_YELLOW:  3,
    SignalPhase.EW_GREEN:  20,
    SignalPhase.EW_YELLOW:  3,
}

# Next phase in the fixed cycle.
_NEXT_PHASE: dict[SignalPhase, SignalPhase] = {
    SignalPhase.NS_GREEN:  SignalPhase.NS_YELLOW,
    SignalPhase.NS_YELLOW: SignalPhase.EW_GREEN,
    SignalPhase.EW_GREEN:  SignalPhase.EW_YELLOW,
    SignalPhase.EW_YELLOW: SignalPhase.NS_GREEN,
}


class TrafficLightAgent(Agent):
    """Stateless agent that drives the fixed-cycle traffic light.

    Each tick it inspects world_state.intersection.phase_timer.  When the
    timer has reached zero it returns the next SignalPhase; otherwise it
    returns None (hold current phase).  The engine applies the transition
    and resets the timer using PHASE_DURATIONS.
    """

    def decide(self, world_state: "WorldState") -> Optional[SignalPhase]:
        """Return the next SignalPhase if the timer expired, else None."""
        intersection = world_state.intersection
        if intersection.phase_timer == 0:
            return _NEXT_PHASE[intersection.signal_phase]
        return None
