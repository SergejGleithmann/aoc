from typing import TypeVar


T = TypeVar("T")


def parse(s: str) -> tuple[list[str]]:
    s = s.split("\n\n")

    def range_to_tuple(x):
        a, b = x.split("-")
        return (int(a), int(b))

    fresh = [range_to_tuple(x) for x in s[0].split("\n")]
    available = [int(x) for x in s[1].split("\n") if x]
    return fresh, available


with open("aoc/2025/day05/resources/input.txt", "r") as file:
    data = parse(file.read())


with open("aoc/2025/day05/resources/test.txt", "r") as file:
    test = parse(file.read())


def spoiled(fresh: list[tuple[int, int]], item: int) -> bool:
    for a, b in fresh:
        if a <= item <= b:
            return False
    return True


def check_all(fresh: list[tuple[int, int]], items: list[int]) -> list[int]:
    return [item for item in items if not spoiled(fresh, item)]


def total_fresh(fresh_lists: list[tuple[int, int]]) -> int:
    res = []
    for a, b in fresh_lists:
        i = 0
        while i < len(res):
            x, y = res[i]
            if x <= b + 1 and a - 1 <= y:
                res[i : i + 1] = []
                a, b = (min(a, x), max(b, y))
            else:
                i += 1
        res.append((a, b))
    print(res)
    return sum([b - a + 1 for a, b in res])


print(len(check_all(*test)))
print(len(check_all(*data)))

print(total_fresh(test[0]))
print(total_fresh(data[0]))
