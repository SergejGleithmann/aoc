import re
from functools import cache


@cache
def build_design(design):
    # recursively build input

    total = 0
    for p in patterns:
        if re.match(p, design):
            if len(p) == len(design):
                total += 1
            else:
                total += build_design(design[len(p) :])
    return total


with open("aoc/2024/day19/resources/data.txt", "r") as f:
    in1, in2 = f.read().split("\n\n")

patterns = re.findall(r"\w+", in1)

total = 0
for design in in2.split("\n"):
    total += build_design(design)
print(total)
