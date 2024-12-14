from copy import copy
from functools import reduce
import re
from typing import Dict, List, Self, Tuple
import numpy as np


class Point(tuple):
    def __add__(self, other: Self) -> Self:
        return Point(x + y for x, y in zip(self, other))

    def __rmul__(self, other: int) -> Self:
        return Point(other * x for x in self)

    def __mod__(self, other: Self) -> Self:
        return Point(x % y for x, y in zip(self, other))


with open("aoc/2024/day14/resources/data.txt", "r") as file:
    data = file.readlines()
dim = Point((101, 103))

""" with open("aoc/2024/day14/resources/test.txt", "r") as file:
    data = file.readlines()
dim = Point((11, 7)) """

robots = [
    (
        Point((int(m.group("px")), int(m.group("py")))),
        Point((int(m.group("vx")), int(m.group("vy")))),
    )
    for robot in data
    if (
        m := re.match(
            r"p=(?P<px>(\+|-)?\d+),(?P<py>(\+|-)?\d+) v=(?P<vx>(\+|-)?\d+),(?P<vy>(\+|-)?\d+)\n",
            robot,
        )
    )
]


def get_quadrants_by_moves(
    robots, dimension: Point, moves: int
) -> Tuple[Tuple[int, int]]:
    quad = [0] * 4
    for robot in robots:
        pos = (robot[0] + moves * robot[1]) % dimension
        q = [None, None]
        for i in range(len(q)):
            if pos[i] < dimension[i] // 2:
                q[i] = 0
            elif pos[i] > dimension[i] // 2:
                q[i] = 1
            else:
                break
        if None not in q:
            quad[q[0] + 2 * q[1]] += 1
    return quad


robots2 = [
    [
        Point((int(m.group("px")), int(m.group("py")))),
        Point((int(m.group("vx")), int(m.group("vy")))),
    ]
    for robot in data
    if (
        m := re.match(
            r"p=(?P<px>(\+|-)?\d+),(?P<py>(\+|-)?\d+) v=(?P<vx>(\+|-)?\d+),(?P<vy>(\+|-)?\d+)\n",
            robot,
        )
    )
]


def check(field):
    l = 10
    for i in range(len(field) - l):
        for j in range(len(field[0]) - l):
            violation = False
            for k in range(l):
                if field[j][i + k] == 0 or field[j + k][i] == 0:
                    violation = True
                    break
            if not violation:
                return True
    return False


def pprint(robots, dim):
    field = [[0] * dim[0] for _ in range(dim[1])]
    print(len(field), len(field[0]))
    for robot in robots:
        field[robot[0][1]][robot[0][0]] += 1
    if check(field):
        print(
            "\n".join(
                [
                    "".join([str(entry) if entry != 0 else " " for entry in row])
                    for row in field
                ]
            )
        )
        input()


def iteration(robots, dimension):
    for id, robot in enumerate(robots):
        robots[id][0] = (robot[0] + robot[1]) % dimension


# Test w/ single Robot from examle
rb = [(Point((2, 4)), Point((2, -3)))]
print(get_quadrants_by_moves(rb, Point((11, 7)), 3))


print(reduce(lambda x, y: x * y, get_quadrants_by_moves(robots, dim, 100)))

for i in range(100000):
    print(f"Iteration {i+1}")
    pprint(robots2, dim)
    iteration(robots2, dim)
