from functools import reduce
import re

with open("aoc/2023/day06/data.txt", "r") as file:
    data = file.read()


def parse(data: str):
    res = re.split(r"\W+", data.strip())
    return list(
        zip(
            [int(x) for x in res[1 : len(res) // 2]],
            [int(x) for x in res[len(res) // 2 + 1 :]],
        )
    )


def parse_one(data: str):
    res = re.split(r"\W+", data.replace(" ", ""))
    return list(
        zip(
            [int(x) for x in res[1 : len(res) // 2] if x != ""],
            [int(x) for x in res[len(res) // 2 + 1 :] if x != ""],
        )
    )


def calc(time, dist):
    res = 0
    for x in range(1, time + 1):
        if (time - x) * x >= dist:
            res += 1
    return res


print(reduce(lambda x, y: x * y, [calc(*x) for x in parse(data)]))
print(reduce(lambda x, y: x * y, [calc(*x) for x in parse_one(data)]))
