type keylock = tuple[int, int, int, int, int]


def translate(candidate: list[str]) -> keylock:
    res = [0, 0, 0, 0, 0]
    assert len(candidate) == 7
    for l in candidate[1:-1]:
        for idx, p in enumerate(l):
            if p == "#":
                res[idx] += 1
    return tuple(res)


def parse_input(data: str) -> tuple[keylock, keylock]:
    keys, locks = [], []
    items = data.split("\n\n")
    for item in items:
        candidate = item.strip().split("\n")
        (locks if candidate[0] == "#####" else keys).append(translate(candidate))
    return keys, locks


with open("aoc/2024/day25/resources/data.txt", "r") as file:
    KEYS, LOCKS = parse_input(file.read())

""" with open("aoc/2024/day25/resources/test.txt", "r") as file:
    KEYS, LOCKS = parse_input(file.read()) """


def combo(keys: list[keylock], locks: list[keylock]) -> list[tuple[keylock, keylock]]:
    res = []
    for key in keys:
        for lock in locks:
            if max([x + y for x, y in zip(key, lock)]) < 6:
                res.append((key, lock))
    return res


# print(KEYS, LOCKS)
print(len(combo(KEYS, LOCKS)))
# print(combo([(0, 5, 3, 4, 3)], [(5, 0, 2, 1, 3)]))
# print(combo([(0, 5, 3, 4, 3)], [(3, 0, 2, 0, 1)]))
