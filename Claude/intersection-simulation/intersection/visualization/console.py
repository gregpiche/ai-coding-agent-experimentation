from intersection.agents.traffic_light_agent import SignalPhase
from intersection.visualization.renderer import Renderer
from intersection.world.lane import Direction

GRID = 21
CENTER = 10
RESET = "\033[0m"

_ARROWS = {
    Direction.NORTH: "↓",
    Direction.SOUTH: "↑",
    Direction.EAST: "←",
    Direction.WEST: "→",
}


def _vehicle_coords(v) -> tuple[int, int]:
    p = v.position
    if v.direction == Direction.NORTH:
        return (p, CENTER - 1)            # col 9
    if v.direction == Direction.SOUTH:
        return (GRID - 1 - p, CENTER + 1) # col 11
    if v.direction == Direction.EAST:
        return (CENTER - 1, GRID - 1 - p) # row 9
    return (CENTER + 1, p)                # WEST: row 11


def _vehicle_color(phase: SignalPhase, direction: Direction) -> str:
    if direction in (Direction.NORTH, Direction.SOUTH):
        if phase == SignalPhase.NS_GREEN:
            return "\033[32m"
        if phase == SignalPhase.NS_YELLOW:
            return "\033[33m"
        return "\033[31m"
    else:
        if phase == SignalPhase.EW_GREEN:
            return "\033[32m"
        if phase == SignalPhase.EW_YELLOW:
            return "\033[33m"
        return "\033[31m"


class ConsoleRenderer(Renderer):
    def __init__(self, clear_screen: bool = True) -> None:
        self.clear_screen = clear_screen

    def render(self, world_state) -> None:
        if self.clear_screen:
            print("\033[2J\033[H", end="")

        phase = world_state.intersection.signal_phase
        timer = world_state.intersection.phase_timer
        print(f"=== Tick {world_state.tick:3d} | {phase.name:<10} ({timer}t) ===\n")

        # Build grid: plain chars (no ANSI) + separate color layer
        grid_char = [[" "] * GRID for _ in range(GRID)]
        grid_color = [[""] * GRID for _ in range(GRID)]

        # Road background: 3-cell-wide roads with center dividers
        for i in range(GRID):
            # NS road lanes (cols 9, 11) and divider (col 10)
            for col in (CENTER - 1, CENTER, CENTER + 1):
                row = i
                in_intersection = (CENTER - 1 <= row <= CENTER + 1)
                if in_intersection:
                    grid_char[row][col] = "+"
                    is_corner = (row in (CENTER - 1, CENTER + 1)) and (col in (CENTER - 1, CENTER + 1))
                    if is_corner:
                        if row == CENTER - 1 and col == CENTER - 1:
                            corner_dir = Direction.NORTH
                        elif row == CENTER + 1 and col == CENTER + 1:
                            corner_dir = Direction.SOUTH
                        elif row == CENTER - 1 and col == CENTER + 1:
                            corner_dir = Direction.EAST
                        else:
                            corner_dir = Direction.WEST
                        grid_color[row][col] = _vehicle_color(phase, corner_dir)
                elif col == CENTER:
                    grid_char[row][col] = "|"
                else:
                    grid_char[row][col] = "·"

            # EW road lanes (rows 9, 11) and divider (row 10) — skip intersection cols
            for row in (CENTER - 1, CENTER, CENTER + 1):
                col = i
                if CENTER - 1 <= col <= CENTER + 1:
                    continue  # already set above
                if row == CENTER:
                    grid_char[row][col] = "─"
                else:
                    grid_char[row][col] = "·"

        # Vehicles
        for v in world_state.vehicles:
            row, col = _vehicle_coords(v)
            if 0 <= row < GRID and 0 <= col < GRID:
                grid_char[row][col] = _ARROWS[v.direction]
                grid_color[row][col] = _vehicle_color(phase, v.direction)

        # Print N label above grid
        n_indent = " " * (4 + CENTER)  # 4 chars for "W → " prefix
        print(f"{n_indent}N")

        # Print rows
        for row in range(GRID):
            cells = []
            for col in range(GRID):
                ch = grid_char[row][col]
                color = grid_color[row][col]
                if color:
                    cells.append(f"{color}{ch}{RESET}")
                else:
                    cells.append(ch)

            row_str = "".join(cells)
            if row == CENTER:
                print(f"W → {row_str} ← E")
            else:
                print(f"    {row_str}")

        # Print S label below grid
        print(f"{n_indent}S")

        print(f"\n  Vehicles: {len(world_state.vehicles)}")
