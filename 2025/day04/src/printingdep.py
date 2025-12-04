import time
import os
from typing import Callable, TypeVar, Generic


with open("aoc/2025/day04/resources/input.txt", "r") as file:
    data = file.read()


with open("aoc/2025/day04/resources/test.txt", "r") as file:
    test = file.read()


clear = lambda: os.system("cls")


T = TypeVar("T")


def parse(s: str) -> list[list[str]]:
    """Parses a string into a list of characters nested in a list of lines.

    Args:
        s (str): input string

    Returns:
        list[list[str]]: list of lists of characters
    """
    return [[x for x in line] for line in s.split("\n")]


def neighbours(field: list[list[T]], i, j) -> list[T]:
    """Determines all neighbours of the cell in bounds of field.

    Args:
        field (list[list[T]]): 2 d array
        i (_type_): row index
        j (_type_): column index

    Returns:
        list[T]: contents of the neighbour cells
    """
    deltas = [-1, 0, 1]
    neighbour_poss = [
        (i + di, j + dj) for di in deltas for dj in deltas if dj != 0 or di != 0
    ]

    return [
        field[ni][nj]
        for ni, nj in neighbour_poss
        if (0 <= ni < len(field)) and (0 <= nj < len(field[0]))
    ]


def access(field: list[list[T]], token: T = "@") -> list[tuple[int, int, int]]:
    """Determines how many items are in vincinity.

    Args:
        field (list[list[T]]): 2 d array to search
        token (T, optional): item to search for. Defaults to "@".

    Returns:
        list[tuple[int, int, int]]: list containing the number of items in vincity for each item together with its position.
    """
    proxy_map = []
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == token:
                proxy_map.append(
                    (
                        len([x for x in neighbours(field, i, j) if x == token]),
                        i,
                        j,
                    )
                )
    return proxy_map


def pprint(field: list[list[T]]) -> None:
    """Pretty print a 2d list

    Args:
        field (list[list[T]]): 2 dimensional list
    """
    print("\n".join(map(lambda x: "".join(x), [map(str, line) for line in field])))


def update_field(
    field: list[list[T]], idxs: list[tuple[int, int, int]], value: T = "."
) -> list[list[T]]:
    """Updates a two d array at given positions with given value. Mutates the given array!

    Args:
        field (list[list[T]]): 2 d array (will be mutated!)
        idxs (list[tuple[int, int, int]]): list of positions to update
        value (T, optional): Value the given positions are set to. Defaults to ".".

    Returns:
        list[list[T]]: Updated 2-d array (same object as input)
    """
    for _, i, j in idxs:
        field[i][j] = value
    return field


def iterative_removal(field: list[list[T]], visual: bool = False) -> int:
    """Removes accessible papers until no accessible papers are left and returns the number of removed papers

    Args:
        field (list[list[T]]): 2 d array
        visual (bool): Whether visual output should be printed to console. Defaults to False.

    Returns:
        int: number of removed items
    """
    if visual:
        clear()
        pprint(field)
        time.sleep(0.2)

    accessible = [x for x in access(field) if x[0] < 4]
    if len(accessible) > 0:
        return len(accessible) + iterative_removal(
            update_field(field, accessible), visual=visual
        )
    else:
        return 0


print(len([x for x, i, j in access(parse(test)) if x < 4]))
print(len([x for x, i, j in access(parse(data)) if x < 4]))

print(iterative_removal(parse(test)))
print("letsgo")
print(iterative_removal(parse(data), visual=True))
