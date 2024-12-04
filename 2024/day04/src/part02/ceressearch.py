from typing import List


with open("aoc/2024/day04/resources/data.txt", "r") as file:
    data = file.read()

""" 
with open("aoc/2024/day04/resources/test.txt", "r") as file:
    data = file.read() 
"""
df = data.split("\n")


def check_xmas_pos(df: List[str], i: int, j: int) -> int:

    return (
        df[i][j] == "A"
        and (
            (df[i + 1][j + 1] == "M" and df[i - 1][j - 1] == "S")
            or (df[i + 1][j + 1] == "S" and df[i - 1][j - 1] == "M")
        )
        and (
            (df[i + 1][j - 1] == "M" and df[i - 1][j + 1] == "S")
            or (df[i + 1][j - 1] == "S" and df[i - 1][j + 1] == "M")
        )
    )


def xmas_count(df: List[str]) -> int:
    res = 0
    l = len(df)
    for i in range(1, l - 1):
        for j in range(1, l - 1):
            res += check_xmas_pos(df, i, j)
    return res


print(xmas_count(df))
