with open("aoc/2025/day08/resources/input.txt", "r") as file:
    data = [tuple(map(int, p.split(","))) for p in file.readlines()]


with open("aoc/2025/day08/resources/test.txt", "r") as file:
    test = [tuple(map(int, p.split(","))) for p in file.readlines()]


print(test)
