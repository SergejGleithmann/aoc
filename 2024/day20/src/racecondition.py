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


class Map[X](list[list[X]]):
    def update(self, p: Point, value: X) -> None:
        self[p[1]][p[0]] = value

    def get(self, p: Point) -> X:
        return self[p[1]][p[0]]

    def dim(self):
        return Point((len(self[0]), len(self)))

    def __str__(self) -> str:
        return "\n".join(["".join(map(str, row)) for row in self])


with open("aoc/2024/day20/resources/data.txt", "r") as file:
    data = file.readlines()

with open("aoc/2024/day20/resources/test.txt", "r") as file:
    data = file.readlines()


track = Map([[[c, -1] for c in line.strip()] for line in data])

DIRS = (
    Point((1, 0)),
    Point((0, 1)),
    Point((-1, 0)),
    Point((0, -1)),
)


def get_pos(track):
    dim = Point((len(track), len(track[0])))
    for i in range(dim[0]):
        for j in range(dim[1]):
            match track[j][i][0]:
                case "S":
                    start = Point((i, j))
                case "E":
                    end = Point((i, j))
    return dim, start, end


DIM, START, END = get_pos(track)


def run(track):
    pos = START
    time = 0
    track.update(pos, ("S", 0))
    while track.get(pos)[0] != "E":
        time += 1
        for d in DIRS:
            if (
                (new_pos := (pos + d)).in_bounds(DIM)
                and track.get(new_pos)[0] != "#"
                and track.get(new_pos)[1] == -1
            ):
                track.update(new_pos, [track.get(new_pos)[0], time])
                pos = new_pos
                break


MINSKIP = 100


def get_skips(pos: Point, track: Map):
    if track.get(pos)[1] < 0:
        return set()
    s0 = track.get(pos)[1] + 2
    res = set()
    for d1 in DIRS:
        if (new_pos1 := (pos + d1)).in_bounds(DIM) and track.get(new_pos1)[0] == "#":
            for d2 in DIRS:
                # if (new_pos2 := (new_pos1 + d2)).in_bounds(DIM):
                # print(new_pos2, track.get(new_pos2), s0)
                if (new_pos2 := (new_pos1 + d2)).in_bounds(DIM) and track.get(new_pos2)[
                    1
                ] >= s0 + MINSKIP:
                    """print(
                        pos, track.get(pos), (pos + d1 + d2), track.get(pos + d1 + d2)
                    )"""
                    res.add((pos, new_pos2))
    return res


def get_longskips(pos: Point, track: Map, dist: int, dirs: list[Point]):
    res = set()
    for v in dirs:
        new_pos = v + pos
        assert abs(pos[0] - new_pos[0]) + abs(pos[1] - new_pos[1]) == dist
        if (
            new_pos.in_bounds(DIM)
            and track.get(new_pos)[0] != "#"
            and track.get(new_pos)[1] >= track.get(pos)[1] + MINSKIP + dist
        ):
            # print(v)
            # print(pos, track.get(pos), (new_pos), track.get(new_pos))
            res.add((pos, new_pos))
    return res


def get_longskips2(pos: Point, track: Map, dist: int):
    res = set()
    for i in range(DIM[0]):
        for j in range(DIM[1]):
            new_pos = Point((i, j))
            if abs(pos[0] - new_pos[0]) + abs(pos[1] - new_pos[1]) == dist:
                assert abs(pos[0] - new_pos[0]) + abs(pos[1] - new_pos[1]) == dist
                if (
                    new_pos.in_bounds(DIM)
                    and track.get(new_pos)[0] != "#"
                    and track.get(new_pos)[1] >= track.get(pos)[1] + MINSKIP
                ):
                    # print(pos, track.get(pos), (new_pos), track.get(new_pos))
                    res.add((pos, new_pos))
    return res


def get_all_skips(track):
    res = set()
    for i in range(DIM[0]):
        for j in range(DIM[1]):
            pos = Point((i, j))
            res |= get_skips(pos, track)
    return res


def get_all_longskips(track: Map, dist: int):
    vectors = {
        v
        for group in [
            [
                Point((i, (dist - i))),
                Point((i, -(dist - i))),
                Point((-i, (dist - i))),
                Point((-i, -(dist - i))),
            ]
            for i in range(dist + 1)
        ]
        for v in group
    }
    # print(vectors)
    input()
    res = set()
    for i in range(DIM[0]):
        # print(i)
        for j in range(DIM[1]):

            pos = Point((i, j))
            if track.get(pos)[0] != "#":
                res |= get_longskips(pos, track, dist, vectors)
    return res


run(track)
print(track.get(END))
# print(track)
print(len(get_all_skips(track)))
print(len(get_all_longskips(track, 2)))
""" print("-------------")
print(
    get_longskips(
        Point((8, 7)),
        track,
        2,
        {
            v
            for group in [
                [
                    Point((i, (2 - i))),
                    Point((i, -(2 - i))),
                    Point((-i, (2 - i))),
                    Point((-i, -(2 - i))),
                ]
                for i in range(2 + 1)
            ]
            for v in group
        },
    )
)
print(get_skips(Point((8, 7)), track)) """
