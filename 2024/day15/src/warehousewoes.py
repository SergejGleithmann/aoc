from typing import List, Self


class Point(tuple[int, int]):
    def __add__(self, other: Self) -> Self:
        return Point(x + y for x, y in zip(self, other))

    def __rmul__(self, other: int) -> Self:
        return Point(other * x for x in self)

    def __mod__(self, other: Self) -> Self:
        return Point(x % y for x, y in zip(self, other))


class Map(list[list[str]]):
    def update(self, p: Point, value: str) -> None:
        self[p[1]][p[0]] = value

    def get(self, p: Point) -> str:
        return self[p[1]][p[0]]

    def dim(self):
        return Point((len(self[0]), len(self)))

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self])


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

map = Map([list(line) for line in str_map.split("\n")])

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


move_all(map, moves)
print(get_gps(map))

move_all(map_l, moves, True)
print(get_gps(map_l))
