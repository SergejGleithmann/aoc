from functools import reduce
import re
from typing import Dict, List, Tuple


with open("aoc/2023/day02/data.txt", "r") as file:
    data = file.readlines()

type Set = Dict[str, int]
type Game = Tuple[int, List[Set]]


def parse_moves(games: str) -> Game:
    return (
        int(re.match(r"Game (\d+)", games[0]).group(1)),
        [
            {(ct := color.split(" "))[1]: int(ct[0]) for color in set.split(", ")}
            for set in games[1].split("; ")
        ],
    )


df = [parse_moves(line[:-1].split(": ")) for line in data if line != "\n"]


def get_max_of(sets: List[Set], colors: List[str]) -> Set:
    max_colors = {color: 0 for color in colors}
    for set in sets:
        for color in colors:
            max_colors[color] = max([max_colors[color], set.get(color, 0)])
    return max_colors


def is_possible(sets: List[Set], numbers: Set) -> bool:
    max_colors = get_max_of(sets, numbers.keys())
    print(sets, max_colors)
    for color, count in max_colors.items():
        if count > numbers[color]:
            return False
    return True


def count_possible(games: List[Game], numbers: Set) -> int:
    return sum([id for id, sets in games if is_possible(sets, numbers)])


# print(df)
print(count_possible(df, {"red": 12, "green": 13, "blue": 14}))
""" print(
    is_possible(
        [
            {"blue": 3, "red": 2},
            {"blue": 1, "green": 3, "red": 3},
            {"red": 1, "green": 3},
            {"green": 2, "red": 2, "blue": 2},
        ],
        {"red": 12, "green": 13, "blue": 14},
    )
) """

print(
    sum(
        [
            reduce(
                lambda x, y: x * y, get_max_of(sets, ["red", "green", "blue"]).values()
            )
            for _id, sets in df
        ]
    )
)
