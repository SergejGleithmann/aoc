from math import prod
import re

type Piece = list[list[bool]]
type Field = list[dict[str, tuple[int, ...]]]


def parse_part(s: str) -> list[list[bool]]:
    splitted = s.split("\n")
    return [[c == "#" for c in line] for line in splitted[1:]]


def parse(
    s: str,
) -> dict[str, dict[int, Piece | Field]]:
    splitted = s.strip().split("\n\n")

    return {
        "pieces": {int(part[0]): parse_part(part) for part in splitted[:-1]},
        "fields": [
            {"dim": (int(m[1]), int(m[2])), "pieces": tuple(map(int, m[3].split(" ")))}
            for field in splitted[-1].split("\n")
            if (m := re.match(r"(\d+)x(\d+): ([0-9 ]+)", field))
        ],
    }


with open("aoc/2025/day12/resources/input.txt", "r") as file:
    data = parse(file.read())


with open("aoc/2025/day12/resources/test.txt", "r") as file:
    test = parse(file.read())


def can_fit_space(pieces: list[Piece], field: list[Field]) -> bool:
    return prod(field["dim"]) >= sum(
        [sum(map(sum, pieces[i])) * count for i, count in enumerate(field["pieces"])]
    )


def fits_naive(field: list[Field]) -> bool:
    return prod(field["dim"]) >= sum([9 * count for count in field["pieces"]])


print(len(data["fields"]))
print(sum([fits_naive(field) for field in data["fields"]]))
print(sum([can_fit_space(data["pieces"], field) for field in data["fields"]]))
