# Defines IntersectionState: the signal phase (NS_GREEN, NS_YELLOW, EW_GREEN, EW_YELLOW) and the phase timer countdown for the four-way intersection.

from __future__ import annotations

from dataclasses import dataclass

from intersection.agents.traffic_light_agent import SignalPhase


@dataclass
class IntersectionState:
    signal_phase: SignalPhase
    phase_timer: int  # ticks remaining in current phase
