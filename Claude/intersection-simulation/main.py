import time
from intersection.world.state import WorldState
from intersection.world.intersection import IntersectionState
from intersection.world.lane import Direction, Lane
from intersection.agents.traffic_light_agent import TrafficLightAgent, SignalPhase, PHASE_DURATIONS
from intersection.engine.spawner import Spawner
from intersection.engine.simulation import SimulationEngine
from intersection.visualization import ConsoleRenderer

TICKS       = 100
TICK_DELAY  = 0.15   # seconds between frames (0 = as fast as possible)
SPAWN_RATE  = 0.3
SEED        = 42

def build_initial_world() -> WorldState:
    initial_phase = SignalPhase.NS_GREEN
    return WorldState(
        tick=0,
        vehicles=[],
        intersection=IntersectionState(
            signal_phase=initial_phase,
            phase_timer=PHASE_DURATIONS[initial_phase],
        ),
        lanes={d: Lane(direction=d) for d in Direction},
    )

def main() -> None:
    world    = build_initial_world()
    engine   = SimulationEngine(world, TrafficLightAgent(), Spawner(SPAWN_RATE, SEED))
    renderer = ConsoleRenderer(clear_screen=True)

    for _ in range(TICKS):
        engine.tick()
        renderer.render(world)
        if TICK_DELAY > 0:
            time.sleep(TICK_DELAY)

if __name__ == "__main__":
    main()
