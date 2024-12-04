from typing import List


with open("aoc/2024/day04/resources/data.txt", "r") as file:
    data = file.read()

""" 
with open("aoc/2024/day04/resources/test.txt", "r") as file:
    data = file.read() 
"""
df = data.split("\n")


def check_xmas(letters: List[str]) -> bool:
    return (
        letters[0] == "X"
        and letters[1] == "M"
        and letters[2] == "A"
        and letters[3] == "S"
    ) or (
        letters[0] == "S"
        and letters[1] == "A"
        and letters[2] == "M"
        and letters[3] == "X"
    )


def check_xmas_pos(df: List[str], i: int, j: int) -> int:
    res = 0
    pad_i = i < len(df) - 3
    pad_j = j < len(df) - 3
    if pad_j:
        res += int(check_xmas([df[i][j + x] for x in range(4)]))
    if pad_i:
        res += int(check_xmas([df[i + x][j] for x in range(4)]))
    if pad_i and pad_j:
        res += int(check_xmas([df[i + x][j + x] for x in range(4)]))
    if j >= 3 and pad_i:
        res += int(check_xmas([df[i + x][j - x] for x in range(4)]))

    return res


def xmas_count(df: List[str]) -> int:
    res = 0
    l = len(df)
    for i in range(l):
        for j in range(l):
            res += check_xmas_pos(df, i, j)
    return res


print(xmas_count(df))
