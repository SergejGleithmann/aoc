import re
import operator

with open("aoc/2024/day03/resources/data.txt", "r") as file:
    data = file.read()


def apply_mult(data: str) -> int:
    matches = re.findall(r"mul\((\d+),(\d+)\)", data)
    return sum(map(lambda args: operator.mul(*map(int, args)), matches))


print(apply_mult(data))
