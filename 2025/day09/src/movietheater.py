with open("aoc/2025/day09/resources/input.txt", "r") as file:
    data = [tuple(map(int, p.split(","))) for p in file.readlines()]


with open("aoc/2025/day09/resources/test.txt", "r") as file:
    test = [tuple(map(int, p.split(","))) for p in file.readlines()]


def getrect(a: int, b: int) -> tuple[tuple[int, int], tuple[int, int]]:
    return (min(a[0], b[0]), max(a[0], b[0])), (min(a[1], b[1]), max(a[1], b[1]))


def check_rec(
    pair: tuple[tuple[int, int], tuple[int, int]], border: list[tuple[int, int]]
) -> bool:
    (rxmin, rxmax), (rymin, rymax) = getrect(*pair)
    for i in range(-1, len(border)):
        x1, y1 = border[i - 1]
        x2, y2 = border[i]
        if (
            rxmin < max(x1, x2)
            and rxmax > min(x1, x2)
            and rymin < min(y1, y2)
            and rymax > max(y1, y2)
        ):
            return False
    return True


def area(a: int, b: int) -> int:
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def part2(points: list[tuple[int, int]]) -> int:
    max_area = 0
    pairs = [(a, b) for a in points for b in points if a != b]
    for pair in pairs:
        temp_area = area(*pair)
        if temp_area > max_area:
            if check_rec(pair, points):
                max_area = max(area(*pair), max_area)
    return max_area


print(part2(test))
print(part2(data))
