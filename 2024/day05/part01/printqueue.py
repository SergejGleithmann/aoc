from typing import List, Tuple


with open("aoc/2024/day05/resources/data.txt", "r") as file:
    data = file.read()

""" with open("aoc/2024/day05/resources/test.txt", "r") as file:
    data = file.read() """

rules_raw, updates_raw = data.split("\n\n")
rules: List[Tuple[int]] = list(
    map(lambda x: tuple(map(int, x.split("|"))), rules_raw.split("\n"))
)
updates: List[List[int]] = list(
    map(lambda x: list(map(int, x.split(","))), updates_raw[:-1].split("\n"))
)


def check_update(update: List[int]) -> bool:
    l = len(update)
    for i in range(l):
        for j in range(i + 1, l):
            if (update[j], update[i]) in rules:
                return False
    return True


def sum_of_middle_printed(updates: List[List[int]]) -> int:
    return sum(map(lambda x: x[len(x) // 2], filter(check_update, updates)))


print(sum_of_middle_printed(updates))
