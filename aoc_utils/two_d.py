from typing import Self


class Point(tuple[int, int]):
    def __add__(self, other: Self) -> Self:
        return Point(x + y for x, y in zip(self, other))

    def __rmul__(self, other: int) -> Self:
        return Point(other * x for x in self)

    def __mod__(self, other: Self) -> Self:
        return Point(x % y for x, y in zip(self, other))


class Map(list[list[str]]):
    def update(self, p: Point, value: str) -> None:
        self[p[1]][p[0]] = value

    def get(self, p: Point) -> str:
        return self[p[1]][p[0]]

    def dim(self):
        return Point((len(self[0]), len(self)))

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self])
