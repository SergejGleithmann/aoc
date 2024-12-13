from copy import copy
from functools import reduce
import re
from typing import Dict, List, Self, Tuple
import numpy as np


with open("aoc/2024/day13/resources/data.txt", "r") as file:
    data = file.read()

""" with open("aoc/2024/day13/resources/test.txt", "r") as file:
    data = file.read() """


class Point(tuple):
    def __add__(self, other: Self) -> Self:
        return Point(x + y for x, y in zip(self, other))

    def __rmul__(self, other: int) -> Self:
        return Point(other * x for x in self)


machines = [
    {
        "A": Point((int(m.group("Ax")), int(m.group("Ay")))),
        "B": Point((int(m.group("Bx")), int(m.group("By")))),
        "Prize": Point((int(m.group("Px")), int(m.group("Py")))),
    }
    for machine in data.split("\n\n")
    if (
        m := re.match(
            r"Button A: X(?P<Ax>(\+|-)?\d+), Y(?P<Ay>(\+|-)?\d+)\nButton B: X(?P<Bx>(\+|-)?\d+), Y(?P<By>(\+|-)?\d+)\nPrize: X=(?P<Px>\d+), Y=(?P<Py>\d+)",
            machine,
        )
    )
]


def solve2(machines: Dict[str, int]) -> int:
    res = 0
    for m in machines:
        prize = Point((m["Prize"][0] + 10000000000000, m["Prize"][1] + 10000000000000))

        # Cramersche Regel
        b = int(
            (m["A"][0] * prize[1] - m["A"][1] * prize[0])
            / (m["B"][1] * m["A"][0] - m["B"][0] * m["A"][1])
        )
        # Abkürzung da exakte Lösung unwichtig
        a = int((prize[0] - m["B"][0] * b) / m["A"][0])
        if a >= 0 and b >= 0 and a * m["A"] + b * m["B"] == prize:
            print(a, b)
            res += 3 * a + b
    return res


print(
    sum(
        [
            3 * a + b
            for machine in machines
            for a in range(100)
            for b in range(100)
            if a * machine["A"] + b * machine["B"] == machine["Prize"]
        ]
    )
)

print(solve2(machines))
