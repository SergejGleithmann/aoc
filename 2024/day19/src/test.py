import re
from functools import cache


@cache
def build_design(design):
    # recursively try to build input
    # return 1 if possible, 0 if not possible

    for p in patterns:
        if re.match(p, design):
            if len(p) == len(design):
                return 1
            if build_design(design[len(p) :]):
                return 1
    return 0


@cache
def build_all_design(design):
    # recursively try to build input
    # return 1 if possible, 0 if not possible
    res = 0
    for p in patterns:
        if re.match(p, design):
            if len(p) == len(design):
                res += 1
            else:
                res += build_all_design(design[len(p) :])
    return res


with open("aoc/2024/day19/resources/data.txt", "r") as f:
    in1, in2 = f.read().split("\n\n")

patterns = re.findall(r"\w+", in1)

total = 0
i = 0
for design in in2.split("\n"):
    i += 1
    total += build_all_design(design)
print(total)
