import heapq
import re

from copy import copy
from typing import Self

import numpy as np


class Point(tuple[int, int]):
    def __add__(self, other: Self) -> Self:
        return Point(x + y for x, y in zip(self, other))

    def __rmul__(self, other: int) -> Self:
        return Point(other * x for x in self)

    def __mod__(self, other: Self) -> Self:
        return Point(x % y for x, y in zip(self, other))

    def in_bounds(self, other: Self) -> bool:
        return 0 <= self[0] < other[0] and 0 <= self[1] < other[1]


class Map(list[list[str]]):
    def update(self, p: Point, value: str) -> None:
        self[p[1]][p[0]] = value

    def get(self, p: Point) -> str:
        return self[p[1]][p[0]]

    def dim(self):
        return Point((len(self[0]), len(self)))

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self])


with open("aoc/2024/day18/resources/data.txt", "r") as file:
    data = file.readlines()
DIM = Point((71, 71))
END = Point((70, 70))

""" with open("aoc/2024/day18/resources/test.txt", "r") as file:
    data = file.readlines()
DIM = Point((71, 71))
END = Point((70, 70)) """


START = Point((0, 0))
positions = [Point(tuple(map(int, line.split(",")))) for line in data]

DIRS = (
    Point((1, 0)),
    Point((0, 1)),
    Point((-1, 0)),
    Point((0, -1)),
)


def get_memspace(data) -> Map:
    memspace = []
    for j in range(DIM[1]):
        memspace.append(["."] * DIM[0])
    memspace = Map(memspace)


def set_obstacles(m: Map):
    for i in range(1024):
        m.update(positions[i], "#")


def dijkstra(map: Map) -> tuple[int, set[Point]]:
    dim = map.dim()
    dist = []
    for _ in range(dim[1]):
        dist.append([[np.inf, set()] for _ in range(dim[0])])

    dist[START[1]][START[0]] = (0, {START})

    pq = []
    heapq.heappush(pq, (0, START))

    while len(pq) > 0:
        score, pos = heapq.heappop(pq)
        if score == np.inf:
            break
        for dir in DIRS:
            new_pos = dir + pos
            if new_pos.in_bounds(dim) and map.get(new_pos) != "#":
                old_score = dist[new_pos[1]][new_pos[0]][0]
                old_path = dist[pos[1]][pos[0]][1]
                if old_score > score + 1:
                    dist[new_pos[1]][new_pos[0]] = (score + 1, old_path | {new_pos})
                    heapq.heappush(pq, (score + 1, new_pos))
    return dist[END[1]][END[0]]


memspace = get_memspace()
set_obstacles(memspace)

### PART 1
print(dijkstra(memspace))
score, path = dijkstra(memspace)
# for pos in path:
#    memspace.update(pos, "O")
# print(memspace)

### PART 2
i = 1023
while score < np.inf:
    i += 1
    print(i)
    memspace.update(positions[i], "#")
    if positions[i] in path:
        score, path = dijkstra(memspace)
print(positions[i])
