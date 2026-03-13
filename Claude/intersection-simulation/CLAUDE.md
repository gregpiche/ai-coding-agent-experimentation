# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Agent-based traffic simulation of a single four-way intersection. Vehicles spawn from all four directions, obey a traffic light controller, and pass through without collisions. The MVP focuses on correctness and simplicity; visualization is optional.

## Environment Setup

This project uses **uv** with Python 3.12. Activate the virtual environment before running anything:

```bash
source .venv/bin/activate
```

No build tooling, test runner, or linting is configured yet — set these up as the project develops (e.g., `pyproject.toml` with pytest and ruff).

## Architecture

Three core components:

### World State
Holds the full simulation snapshot at each tick: `tick`, `vehicles[]`, `intersection` (signal phase + phase timer), and `lanes` (north/south/east/west queues).

### Agents
- **TrafficLightAgent** — fixed-cycle phase rotation: `NS_GREEN (20t) → NS_YELLOW (3t) → EW_GREEN (20t) → EW_YELLOW (3t)`
- **VehicleAgent** — reactive agent; spawns at lane entry, stops on red, moves forward if green and space ahead is free, exits after crossing

### Simulation Engine
Discrete tick loop:
1. Spawn vehicles
2. `traffic_light.update()`
3. `vehicle.decide()` for each vehicle
4. Resolve movements (collision avoidance: no two vehicles in same cell)
5. Remove exited vehicles
6. Advance tick

## Design Principles

1. Simulation must be **deterministic**
2. **Separate** simulation logic from visualization — visualizers read world state, never write it
3. Keep agents **simple and stateless** where possible
4. Prefer **explicit world state** over hidden agent state
5. Design for extensibility toward a 20×20 grid city with additional agent types
