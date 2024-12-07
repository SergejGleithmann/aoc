from typing import List, Tuple


with open("aoc/2024/day06/resources/data.txt", "r") as file:
    data = file.read()

""" with open("aoc/2024/day06/resources/test.txt", "r") as file:
    data = file.read() """


def add_pos(pos1, pos2):
    return tuple(map(lambda x, y: x + y, pos1, pos2))


class GuardedArea:
    orientations = [((-1, 0), "^"), ((0, 1), ">"), ((1, 0), "v"), ((0, -1), "<")]

    def __init__(self, data):
        self.area = [[pos for pos in row] for row in data[:-1].split("\n")]
        print(self.area)
        self.orientation = 0
        i = 0
        self.guard = (0, 0)
        found = False
        while i < len(self.area) and not found:
            j = 0
            while j < len(self.area) and not found:
                # print(f"({i},{j}) - {self.area[i][j]}")
                if self.area[i][j] not in ["#", "."]:
                    self.guard = (i, j)
                    found = True
                j += 1
            i += 1
        print(self.guard)

    def in_bounds(self, i, j):
        return i < len(self.area) and j < len(self.area) and i >= 0 and j >= 0

    def get_pos(self, i, j):
        return self.area[i][j]

    def set_pos(self, i, j, value):
        self.area[i][j] = value

    def move(self):
        or_pos, or_char = GuardedArea.orientations[self.orientation]
        next_pos = add_pos(self.guard, or_pos)
        visited = False
        if not self.in_bounds(*next_pos):
            self.set_pos(*self.guard, "X")
            return -1
        elif self.get_pos(*next_pos) == "#":
            self.orientation = (self.orientation + 1) % 4
            return 0
        else:
            if self.get_pos(*next_pos) == "X":
                visited = True
            self.set_pos(*next_pos, or_char)
            self.set_pos(*self.guard, "X")
            self.guard = next_pos
            return 0 if visited else 1

    def full_movement(self):
        movement = self.move()
        steps = 0
        positions = 1
        while movement >= 0:
            # print(self)
            steps += 1
            positions += movement
            movement = self.move()
        return steps, positions

    def __str__(self):
        return "\n".join(["".join(col) for col in self.area]) + "\n"


print(f"{GuardedArea(data).full_movement()}")
