from functools import reduce
import re
from typing import Dict, List, Tuple


with open("aoc/2023/day03/resources/data.txt", "r") as file:
    data = file.readlines()

df = [line[:-1] for line in data if line != "\n"]


def valid(v):
    return not v.isdigit() and v != "."


for l in range(len(df)):
    idx = 0
    while idx < len(data[l]):
        if data[l][idx].isdigit():
            end = idx + 1
            if data[l][idx - 1] != ".":
                adjecent = True
            while data[l][end].isdigit():
                if valid(data[l][idx - 1]):
                    adjecent = True
                end += 1

        else:
            idx += 1

print(df)
