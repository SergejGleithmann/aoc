import re


def parse(s):
    route, dirs = s.split("\n\n")
    return (
        route,
        {
            m["start"]: {"L": m["l"], "R": m["r"]}
            for dir in dirs.split("\n")
            if (
                m := re.match(
                    r"(?P<start>[A-Z][A-Z][A-Z]) = \((?P<l>[A-Z][A-Z][A-Z]), (?P<r>[A-Z][A-Z][A-Z])\)",
                    dir,
                )
            )
        },
    )


with open("aoc/2023/day08/data.txt", "r") as file:
    data = parse(file.read())

with open("aoc/2023/day08/test.txt", "r") as file:
    test = parse(file.read())


def run(steps: str, dirs: dict[str, dict[str, str]]) -> int:
    i = 0
    current = "AAA"
    while current != "ZZZ":
        current = dirs[current][steps[i % len(steps)]]
        i += 1
    return i


def ghostrun(steps: str, dirs: dict[str, dict[str, str]]):
    allnode = [i for i in dirs.keys() if i[2] == "A"]
    count = 0
    z = 0
    y = []
    e = len(allnode)
    while z < e:
        for direction in dirs:
            for i in range(len(allnode)):
                allnode[i] = dirs[current][steps[i % len(steps)]]
                if direction == "L":
                    allnode[i] = b[a.index(allnode[i])]
                else:
                    allnode[i] = c[a.index(allnode[i])]
            count += 1
            for x in allnode:
                if x[2] == "Z":
                    z += 1
                    allnode.remove(x)
                    y.append(count)


print(reduce(lcm, y))


print(run(*test))
print(run(*data))

print(ghostrun(*test))
print(ghostrun(*data))
