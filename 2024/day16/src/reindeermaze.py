from functools import reduce
import heapq
from typing import List, Self
import numpy as np


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


def in_bounds(p: Point, d: Point) -> bool:
    return 0 <= p[0] < d[0] and 0 <= p[1] < d[1]


DIRS = {
    ">": Point((1, 0)),
    "v": Point((0, 1)),
    "<": Point((-1, 0)),
    "^": Point((0, -1)),
}


with open("aoc/2024/day16/resources/data.txt", "r") as file:
    data = file.readlines()


""" with open("aoc/2024/day16/resources/test.txt", "r") as file:
    data = file.readlines() """


map = Map([[c for c in list(line) if c != "\n"] for line in data])


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
    start, end = None, None
    for y in range(dim[1]):
        for x in range(dim[0]):
            if map[y][x] == "S":
                start = Point((x, y))
            elif map[y][x] == "E":
                end = Point((x, y))
            if start is not None and end is not None:
                break
        if start is not None and end is not None:
            break
    if start is None or end is None:
        raise ValueError("No sarting position found in this map.")
    else:
        return start, end


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


def dijkstra(map: Map):
    dim = map.dim()
    dist = []
    start, end = get_pos(map)
    for _ in range(dim[1]):
        dist.append([[np.inf] * len(DIRS) for _ in range(dim[0])])

    dist[start[1]][start[0]][0] = 0
    dist[start[1]][start[0]][1] = 1000
    dist[start[1]][start[0]][2] = 2000
    dist[start[1]][start[0]][3] = 1000

    pq = []
    heapq.heappush(pq, (0, start, 0))

    while len(pq) > 0:
        score, pos, dir_id = heapq.heappop(pq)
        assert type(dir_id) is int
        if score == np.inf:
            break
        for ndir_id, ndir in enumerate(DIRS.values()):
            new_pos = ndir + pos
            if in_bounds(new_pos, dim) and map.get(new_pos) != "#":
                if ndir_id == dir_id:
                    cost = 0
                elif abs(dir_id - ndir_id) == 2:
                    continue
                else:
                    cost = 1000
                old_score = dist[new_pos[1]][new_pos[0]][ndir_id]
                if old_score > score + cost + 1:
                    dist[new_pos[1]][new_pos[0]][ndir_id] = score + cost + 1
                    heapq.heappush(pq, (score + cost + 1, new_pos, ndir_id))
    return min(dist[end[1]][end[0]])


def dijkstra_path(map: Map):
    dim = map.dim()
    dist = []
    start, end = get_pos(map)
    for _ in range(dim[1]):
        rres = []
        for _ in range(dim[0]):
            dres = []
            for _ in range(len(DIRS)):
                dres.append((np.inf, set()))
            rres.append(dres)
        dist.append(rres)
    dist[start[1]][start[0]][0] = (0, {start})
    dist[start[1]][start[0]][1] = (1000, {start})
    dist[start[1]][start[0]][2] = (2000, {start})
    dist[start[1]][start[0]][3] = (1000, {start})

    pq = []
    heapq.heappush(pq, (0, start, 0))

    while len(pq) > 0:
        score, pos, dir_id = heapq.heappop(pq)
        assert type(dir_id) is int
        if score == np.inf:
            break
        for ndir_id, ndir in enumerate(DIRS.values()):
            new_pos = ndir + pos
            if in_bounds(new_pos, dim) and map.get(new_pos) != "#":
                if ndir_id == dir_id:
                    cost = 0
                elif abs(dir_id - ndir_id) == 2:
                    continue
                else:
                    cost = 1000
                old_score, old_visited = dist[new_pos[1]][new_pos[0]][ndir_id]
                if old_score > score + cost + 1:
                    dist[new_pos[1]][new_pos[0]][ndir_id] = (
                        score + cost + 1,
                        {new_pos} | dist[pos[1]][pos[0]][dir_id][1],
                    )
                    heapq.heappush(pq, (score + cost + 1, new_pos, ndir_id))
                elif old_score == score + cost + 1:

                    dist[new_pos[1]][new_pos[0]][ndir_id] = (
                        old_score,
                        old_visited | dist[pos[1]][pos[0]][dir_id][1],
                    )
    min_val = min([score for score, _path in dist[end[1]][end[0]]])

    return len(
        reduce(
            set.union,
            [path for score, path in dist[end[1]][end[0]] if score == min_val],
        )
    )


print(dijkstra(map))
print(dijkstra_path(map))
