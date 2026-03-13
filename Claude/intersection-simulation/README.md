# ai-agents-intersection

Agent-based traffic simulation of a single four-way intersection. Vehicles spawn from all four directions, obey a fixed-cycle traffic light, and pass through without collisions. Rendered tick-by-tick in the terminal with ANSI color.

## How it works

The simulation runs as a discrete tick loop over shared **world state** (tick counter, vehicle list, signal phase). Two agent types drive behavior:

- **TrafficLightAgent** — rotates through a fixed cycle: `NS_GREEN (20t) → NS_YELLOW (3t) → EW_GREEN (20t) → EW_YELLOW (3t)`
- **VehicleAgent** — reactive agent per vehicle; stops at red, advances on green, and once past the stop line is committed to clearing the intersection regardless of signal changes

Each tick: spawn vehicles → update signal → collect decisions → resolve movements (no two vehicles share a cell) → remove exited vehicles.

## Project structure

```
intersection/
  agents/       # TrafficLightAgent, VehicleAgent
  engine/       # SimulationEngine, Spawner, resolver
  world/        # WorldState, IntersectionState, Lane, Vehicle
  visualization/# ConsoleRenderer (read-only view of world state)
main.py         # Entry point
```

## Setup

Requires Python 3.12 and [uv](https://github.com/astral-sh/uv).

```bash
uv sync
source .venv/bin/activate
```

## Run

```bash
python main.py
```

Runs 100 ticks at 0.15 s/frame. Adjust at the top of `main.py`:

```python
TICKS      = 100   # total ticks to simulate
TICK_DELAY = 0.15  # seconds between frames (0 = as fast as possible)
SPAWN_RATE = 0.3   # probability a vehicle spawns per direction per tick
SEED       = 42    # RNG seed for deterministic output
```
