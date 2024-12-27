from functools import reduce
import re
from typing import Dict, List, Tuple


with open("aoc/2023/day03/data.txt", "r") as file:
    data = file.readlines()
with open("aoc/2023/day03/test.txt", "r") as file:
    test = file.readlines()

df = [line.strip() for line in data if line != "\n"]
dft = [line.strip() for line in test if line != "\n"]


def valid(v):
    return not v.isdigit() and v != "."


def get(df, i, j):
    try:
        return df[i][j]
    except IndexError:
        return "."


def check_adj(df, row, start, end):
    for i in range(start - 1, end + 2):
        if valid(get(df, row - 1, i)) or valid(get(df, row + 1, i)):
            return True
    return valid(get(df, row, start - 1)) or valid(get(df, row, end + 1))


def get_all_valid(df):
    res = []
    for row in range(len(df)):
        start = 0
        end = 0
        idx = 0
        isnum = False
        while idx < len(df[row]):
            if isnum:
                if df[row][idx].isdigit():
                    end += 1
                else:
                    if check_adj(df, row, start, end):
                        res.append(int(df[row][start : end + 1]))
                    isnum = False
            elif df[row][idx].isdigit():
                isnum = True
                start = idx
                end = start
            idx += 1
    return res


print(df)

print(sum(get_all_valid(df)))
print(sum(get_all_valid(dft)))
