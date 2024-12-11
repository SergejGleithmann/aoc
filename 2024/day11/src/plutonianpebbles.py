from copy import copy
from functools import reduce
from typing import List, Set, Tuple


with open("aoc/2024/day11/resources/data.txt", "r") as file:
    data = file.read()

""" with open("aoc/2024/day11/resources/test.txt", "r") as file:
    data = file.read() """

stones = [int(n) for n in data.strip().split(" ")]

# Cache for fast implementation
cache = {}


def blink(stones: List[int]) -> List[int]:
    res = []
    for stone in stones:
        stone_str = str(stone)
        stone_len = len(str(stone_str))
        if stone == 0:
            res.append(1)
        elif stone_len % 2 == 0:
            res.extend(
                [
                    int(stone_str[: stone_len // 2]),
                    int(stone_str[stone_len // 2 :]),
                ]
            )
        else:
            res.append(stone * 2024)
    return res


def blink_fast(num: int, todo: int) -> int:
    if todo == 0:
        return 1
    if (num, todo) in cache:
        return cache[(num, todo)]
    snum = str(num)
    lnum = len(snum)
    if num == 0:
        res = blink_fast(1, todo - 1)
    elif len(snum) % 2 == 0:
        res = blink_fast(int(snum[: lnum // 2]), todo - 1) + blink_fast(
            int(snum[lnum // 2 :]), todo - 1
        )
    else:
        res = blink_fast(num * 2024, todo - 1)

    cache[(num, todo)] = res
    return res


def len_after_blinks(stones: List[int], blinks: int) -> int:
    return sum([blink_fast(stone, blinks) for stone in stones])


""" stones = [125, 17]
while True:
    stones = blink(stones)
    print(stones)
    input() """

# Slow implementation
stones_slow = copy(stones)
for i in range(25):
    stones_slow = blink(stones_slow)
    print(i)
print(len(stones_slow))  # 197357

## Fast implementation
print(len_after_blinks(stones, 25))  # 197357

print(len_after_blinks(stones, 75))  # 234568186890978
