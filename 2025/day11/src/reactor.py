import functools
import math


def parse(s: str) -> tuple[str, list[str]]:
    start, ends = s.strip().split(":")
    return start, ends.strip().split(" ")


with open("aoc/2025/day11/resources/input.txt", "r") as file:
    data = {start: ends for start, ends in map(parse, file.readlines())}

with open("aoc/2025/day11/resources/test-a.txt", "r") as file:
    testa = {start: ends for start, ends in map(parse, file.readlines())}

with open("aoc/2025/day11/resources/test-b.txt", "r") as file:
    testb = {start: ends for start, ends in map(parse, file.readlines())}


# Iterative, slow version
def find_paths(
    network: dict[str, list[str]],
    start: str = "you",
    dest: str = "out",
    cond: list[str] = [],
) -> int:
    todo = [[s] for s in network[start]]
    res = 0
    while todo:
        next_paths = []
        for p in todo:
            if p[-1] != dest and p[-1] != "out":
                next_paths.extend([p + [n] for n in network[p[-1]]])
            elif all([(c in p) for c in cond]):
                res += 1
        todo = next_paths
    return res


# recursive version with caching
def find_paths_rec(
    network: dict[str, list[str]], start: str = "you", dest: str = "out"
) -> int:

    @functools.cache
    def helper(start: str, dest: str) -> int:
        if start == dest:
            return 1
        else:
            return sum([helper(nxt, dest) for nxt in network.get(start, [])])

    return helper(start, dest)


print(find_paths(testa))
print(find_paths(data))

print(find_paths(testb, start="svr", cond=["dac", "fft"]))

# this works because the graph has no loops. Therefore half of the sum is 0.
print(
    math.prod(
        [
            find_paths_rec(data, *route)
            for route in [("svr", "fft"), ("fft", "dac"), ("dac",)]
        ]
    )
    + math.prod(
        [
            find_paths_rec(data, *route)
            for route in [("svr", "dac"), ("dac", "fft"), ("fft",)]
        ]
    )
)
