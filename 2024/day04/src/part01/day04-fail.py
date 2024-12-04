import re
from typing import List, Tuple


with open("aoc/2024/day04/resources/data.txt", "r") as file:
    data = file.read()

with open("aoc/2024/day04/resources/test.txt", "r") as file:
    data = file.read()
df = data.split("\n")


def check_xmas(letters: Tuple[str]) -> bool:
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


def row(df: List[str]) -> int:
    return sum(
        [len(re.findall(r"XMAS", row)) + len(re.findall(r"SAMX", row)) for row in df]
    )


def col(df: List[str]) -> int:
    return sum(
        [
            int(check_xmas((df[j][i], df[j + 1][i], df[j + 2][i], df[j + 3][i])))
            for j in range(len(df) - 3)
            for i in range(len(df))
        ]
    )


def diag(df: List[str]) -> int:
    res = 0
    l = len(df)
    for i in range(3, len(df)):
        for j in range(i - 2):
            res += (
                int(
                    check_xmas(
                        (
                            df[i - j][j],
                            df[i - j - 1][j + 1],
                            df[i - j - 2][j + 2],
                            df[i - j - 3][j + 3],
                        )
                    )
                )
                + int(
                    check_xmas(
                        (
                            df[l - i + j - 1][j],
                            df[l - i + j][j + 1],
                            df[l - i + j + 1][j + 2],
                            df[l - i + j + 2][j + 3],
                        )
                    )
                )
                + int(
                    check_xmas(
                        (
                            df[l - i + j - 1][l - j - 1],
                            df[l - i + j][l - j - 2],
                            df[l - i + j + 1][l - j - 3],
                            df[l - i + j + 2][l - j - 4],
                        )
                    )
                )
                + int(
                    check_xmas(
                        (
                            df[i - j][l - j - 1],
                            df[i - j - 1][l - j - 2],
                            df[i - j - 2][l - j - 3],
                            df[i - j - 3][l - j - 4],
                        )
                    )
                )
            )
            # print(f"{i}-{i-j},{j}") # upper left corner
            # print(f"{i}-{l-i+j-1},{j}")  # lower left corner
            # print(f"{i}-{l-i+j-1},{l - j -1}")  # lower right corner
            # print(f"{i}-{i-j},{l - j -1}")  # lower right corner

    return res


print(row(df))
print(col(df))
print(diag(df))
print(row(df) + col(df) + diag(df))
