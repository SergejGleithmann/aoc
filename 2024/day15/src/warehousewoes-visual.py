import asyncio
from typing import List, Self
import numpy as np
from batgrl.app import App
from batgrl.colors import Color
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.slider import Slider
from batgrl.gadgets.tabs import Tabs
from aoc_utils.theme import AOC_THEME, AocButton, AocText
from aoc_utils.two_d import Point, Map

BROWN = Color.from_hex("44361e")
YELLOW = Color.from_hex("e5da0d")

DIRS = {
    ">": Point((1, 0)),
    "v": Point((0, 1)),
    "<": Point((-1, 0)),
    "^": Point((0, -1)),
}


with open("aoc/2024/day15/resources/data.txt", "r") as file:
    data = file.read()


""" with open("aoc/2024/day15/resources/test.txt", "r") as file:
    data = file.read() """

### Preprocessing
str_map, str_moves = data.split("\n\n")

map = np.array([list(line) for line in str_map.split("\n")])
print(map)
ext = {
    ".": "..",
    "@": "@.",
    "O": "[]",
    "#": "##",
}

map_l = Map(
    [
        [ext_char for char in line for ext_char in ext[char]]
        for line in str_map.split("\n")
    ]
)

moves: List[Point] = [DIRS[move] for move in str_moves if move in DIRS.keys()]

### End of Preprocessing


def get_pos(map: Map) -> Point:
    """Get the position of the robot.

    Args:
        map (Map): Map to get robot position of

    Raises:
        ValueError: If no robot is found.

    Returns:
        Point: Position of robot.
    """
    dim = map.dim()
    for y in range(dim[1]):
        for x in range(dim[0]):
            if map[y][x] == "@":
                return Point((x, y))
    raise ValueError("No Robot found in this map.")


def move(map: Map, pos: Point, dir: Point) -> bool:
    """Moves the symbol at given position along given direction if possible.

    Args:
        map (Map): Map to apply move to
        pos (Point): Position of symbol to move
        dir (Point): Direction of movement

    Returns:
        bool: Whether the move was possible or not.
    """
    dest = pos + dir
    if map.get(dest) == "O":
        if move(map, dest, dir):
            map.update(dest, map.get(pos))
            map.update(pos, ".")
            return True
        else:
            return False
    elif map.get(dest) == ".":
        map.update(dest, map.get(pos))
        map.update(pos, ".")
        return True
    else:
        assert map.get(dest) == "#"
        return False


def move_unchecked(map: Map, pos: Point, dir: Point):
    """Moves the symbol at pos along dir. Mutates the map. Does *not* check if move is legal.

    Args:
        map (Map): Map to mutate
        pos (Point): Starting position
        dir (Point): Direction of movement
    """
    dest = pos + dir
    if map.get(dest) in "[]":
        if dir[1] != 0:
            offset = (-1 if map.get(dest) == "]" else 1, 0)
            move_unchecked(map, dest + offset, dir)
        move_unchecked(map, dest, dir)
    assert map.get(dest) != "#"
    map.update(dest, map.get(pos))
    map.update(pos, ".")


def can_move(map: Map, pos: Point, dir: Point) -> bool:
    """Checks if the symbol at pos can be moved along.

    Args:
        map (Map): Map to check
        pos (Point): Starting position of movement
        dir (Point): Direction of movement

    Returns:
        bool: Whether the move is legal/unblocked.
    """
    dest = pos + dir
    if map.get(dest) == "#":
        return False
    elif map.get(dest) in "[]":
        if dir[1] != 0:
            offset = ((-1 if map.get(dest) == "]" else 1), 0)
            # assert map.get(dest + offset) == "[]" and map.get(dest + offset) in "[]"
            return can_move(map, dest, dir) and can_move(map, dest + offset, dir)
        else:
            return can_move(map, dest, dir)
    else:
        assert map.get(dest) == "."
        return True


def move_all(map: Map, moves: List[Point], large=False):
    """Applys all moves to the map.

    Args:
        map (Map): Map to aplly moves on
        moves (List[Point]): List of directions of movement
        large (bool, optional): Whether the map has 2-Tile boxes (As in Part 2). Defaults to False.
    """
    pos = get_pos(map)
    for m in moves:
        if large:
            if can_move(map, pos, m):
                move_unchecked(map, pos, m)
                pos += m
        else:
            pos = (pos + m) if move(map, pos, m) else pos


def get_dim(map: Map) -> Point:
    """Get the dimensions of the Map

    Args:
        map (Map): Map the dimensions are requested from.

    Returns:
        Point: Maximum values of dimensions as point.
    """
    return Point((len(map[0]), len(map)))


def get_gps(map: Map) -> int:
    """Returns the GPS value of a map according to the

    Args:
        map (Map): _description_

    Returns:
        int: GPS-value
    """
    dim = map.dim()
    return sum(
        [x + 100 * y for x in range(dim[0]) for y in range(dim[1]) if map[y][x] in "[O"]
    )


class WarehouseWoesApp(App):
    async def on_start(self):
        part_1_event = asyncio.Event()
        part_2_event = asyncio.Event()
        delay_1 = 0.07
        delay_2 = 0.07

        start_1 = AocButton("Start", part_1_event.set)
        stop_1 = AocButton("Stop", part_1_event.clear)
        stop_1.left = start_1.right
        slider_label_1 = AocText(
            size=(1, 13), pos_hint={"x_hint": 1.0, "anchor": "right", "x_offset": -10}
        )

        def update_delay_1(value):
            nonlocal delay_1
            delay_1 = value
            slider_label_1.add_str(f" Delay: {value:.2f}")

        slider_1 = Slider(
            size=(1, 10),
            min=0,
            max=0.3,
            start_value=0.07,
            callback=update_delay_1,
            is_transparent=True,
            alpha=0,
            pos_hint={"x_hint": 1.0, "anchor": "right"},
        )
        warehouse_1 = AocText(size=WAREHOUSE_1.shape)
        warehouse_1.canvas["char"] = WAREHOUSE_1
        sv1 = ScrollView(
            pos=(1, 0),
            size_hint={"height_hint": 1.0, "height_offset": -1, "width_hint": 1.0},
            dynamic_bars=True,
        )
        sv1.view = warehouse_1
        container_1 = AocText(size_hint={"height_hint": 1.0, "width_hint": 1.0})
        container_1.add_gadgets(start_1, stop_1, slider_label_1, slider_1, sv1)

        start_2 = AocButton("Start", part_2_event.set)
        stop_2 = AocButton("Stop", part_2_event.clear)
        stop_2.left = start_2.right
        slider_label_2 = AocText(
            size=(1, 13), pos_hint={"x_hint": 1.0, "anchor": "right", "x_offset": -10}
        )

        def update_delay_2(value):
            nonlocal delay_2
            delay_2 = value
            slider_label_2.add_str(f" Delay: {value:.2f}")

        slider_2 = Slider(
            size=(1, 10),
            min=0,
            max=0.3,
            start_value=0.07,
            callback=update_delay_2,
            is_transparent=True,
            alpha=0,
            pos_hint={"x_hint": 1.0, "anchor": "right"},
        )
        warehouse_2 = AocText(size=WAREHOUSE_2.shape)
        warehouse_2.canvas["char"] = WAREHOUSE_2
        sv2 = ScrollView(
            pos=(1, 0),
            size_hint={"height_hint": 1.0, "height_offset": -1, "width_hint": 1.0},
            dynamic_bars=True,
        )
        sv2.view = warehouse_2
        container_2 = AocText(size_hint={"height_hint": 1.0, "width_hint": 1.0})
        container_2.add_gadgets(start_2, stop_2, slider_label_2, slider_2, sv2)

        tabs = Tabs(size_hint={"height_hint": 1.0, "width_hint": 1.0})
        tabs.add_tab("Part 1", container_1)
        tabs.add_tab("Part 2", container_2)
        self.add_gadget(tabs)

        container_1.add_str(
            "Instructions:", truncate_str=True, pos=(0, stop_1.right + 1)
        )
        container_1.canvas["fg_color"][0, 28] = 255
        container_2.add_str(
            "Instructions:", truncate_str=True, pos=(0, stop_2.right + 1)
        )
        container_2.canvas["fg_color"][0, 28] = 255

        def recolor_foreground(warehouse):
            warehouse.canvas["fg_color"] = warehouse.default_fg_color
            warehouse.canvas["fg_color"][
                np.isin(warehouse.canvas["char"], ["O", "[", "]"])
            ] = BROWN

        async def do_part_one():
            current_pos = START
            wh = warehouse_1.canvas["char"]
            for instruction in INSTRUCTIONS:
                container_1.canvas["char"][0, 29:] = container_1.canvas["char"][
                    0, 28:-1
                ]
                container_1.canvas["char"][0, 28] = instruction
                direction = DIRS[instruction]
                warehouse_1.canvas["char"][current_pos] = "."
                new_pos = current_pos + direction
                if wh[new_pos] == ".":
                    current_pos = new_pos
                elif wh[new_pos] == "#":
                    continue

                look_ahead = new_pos
                while wh[look_ahead] == "O":
                    look_ahead += direction
                if wh[look_ahead] == "#":
                    continue
                wh[look_ahead] = "O"
                wh[new_pos] = "."
                current_pos = new_pos

                recolor_foreground(warehouse_1)
                warehouse_1.canvas["char"][current_pos] = "@"
                warehouse_1.canvas["fg_color"][current_pos] = YELLOW
                await part_1_event.wait()
                await asyncio.sleep(delay_1)

        async def do_part_two():
            current_pos = Vec2(START.y, 2 * START.x)
            wh = warehouse_2.canvas["char"]
            for instruction in INSTRUCTIONS:
                container_2.canvas["char"][0, 29:] = container_2.canvas["char"][
                    0, 28:-1
                ]
                container_2.canvas["char"][0, 28] = instruction
                direction = DIRS[instruction]
                warehouse_2.canvas["char"][current_pos] = "."
                new_pos = current_pos + direction
                if wh[new_pos] == ".":
                    current_pos = new_pos
                elif wh[new_pos] == "#":
                    pass
                elif direction.x:  # Horizontal push.
                    look_ahead = new_pos
                    while wh[look_ahead] in "[]":
                        look_ahead += direction
                    if wh[look_ahead] == "#":
                        continue
                    while look_ahead != new_pos:
                        wh[look_ahead] = wh[look_ahead - direction]
                        look_ahead -= direction
                    wh[new_pos] = "."
                    current_pos = new_pos
                elif can_vertical_push(new_pos, direction, wh):
                    do_vertical_push(new_pos, direction, wh)
                    current_pos = new_pos

                recolor_foreground(warehouse_2)
                warehouse_2.canvas["char"][current_pos] = "@"
                warehouse_2.canvas["fg_color"][current_pos] = YELLOW
                await part_2_event.wait()
                await asyncio.sleep(delay_2)

        part_1_task = asyncio.create_task(do_part_one())  # noqa: F841
        part_2_task = asyncio.create_task(do_part_two())  # noqa: F841


move_all(map, moves)
print(get_gps(map))

move_all(map_l, moves, True)
print(get_gps(map_l))
