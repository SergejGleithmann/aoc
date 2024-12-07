from copy import deepcopy
from typing import List, Set, Tuple


with open("aoc/2024/day06/resources/data.txt", "r") as file:
    data = file.read()

""" with open("aoc/2024/day06/resources/test.txt", "r") as file:
    data = file.read() """


def add_pos(pos1, pos2):
    return tuple(map(lambda x, y: x + y, pos1, pos2))


def print_pos(pos: Tuple[str, Set[int]]) -> str:
    str, dirs = pos
    if len(dirs) == 0:
        return str
    elif 1 in dirs or 3 in dirs:
        if 0 in dirs or 2 in dirs:
            return "+"
        else:
            return "-"
    else:
        return "|"


class GuardedArea:
    orientations = [((-1, 0), "^"), ((0, 1), ">"), ((1, 0), "v"), ((0, -1), "<")]

    def __init__(self, area, guard=None, orientation=0):
        self.area = area
        self.orientation = orientation
        i = 0
        if guard:
            self.guard = guard
        else:
            found = False
            while i < len(self.area) and not found:
                j = 0
                while j < len(self.area) and not found:
                    # print(f"({i},{j}) - {self.area[i][j]}")
                    if self.area[i][j][0] not in ["#", "."]:
                        self.guard = (i, j)
                        found = True
                        self.area[i][j][1] = {
                            GuardedArea.orientations[self.orientation]
                        }
                    j += 1
                i += 1

    def copy(self):
        return GuardedArea(deepcopy(self.area), self.guard, self.orientation)

    def in_bounds(self, i, j):
        return i < len(self.area) and j < len(self.area) and i >= 0 and j >= 0

    def get_pos(self, i, j):
        return self.area[i][j]

    def set_pos(self, i, j, value):
        self.area[i][j] = value

    def check_loop(self):
        alternate = self.copy()
        alternate.turn()
        movement, loop = alternate.move(False)
        while movement >= 0:
            movement, loop = alternate.move(False)
        return loop

    def visit_pos(self, i, j):
        self.area[i][j][1].add(self.orientation)

    def turn(self):
        self.orientation = (self.orientation + 1) % 4
        self.visit_pos(*self.guard)

    def get_next_pos(self):
        or_pos, _ = GuardedArea.orientations[self.orientation]
        return add_pos(self.guard, or_pos)

    def move(self, loops=True):
        loop = False
        next_pos = self.get_next_pos()
        visited = False
        if not self.in_bounds(*next_pos):
            return -1, False
        elif self.get_pos(*next_pos)[0] == "#":
            self.turn()
            return 0, False
        else:
            if loops:
                loop = self.check_loop()
            if len(self.get_pos(*next_pos)[1]) > 0:
                visited = True
                if self.orientation in self.get_pos(*next_pos)[1]:
                    return -1, True
            self.visit_pos(*next_pos)
            self.guard = next_pos
            return 0 if visited else 1, loop

    def full_movement(self):
        loops = 0
        movement, loop = self.move()
        steps = 0
        positions = 1
        while movement >= 0:
            loops += int(loop)
            steps += 1
            positions += movement
            movement, loop = self.move()
            if steps % 100 == 0:
                print(steps)
        return steps, positions, loops

    def __str__(self):
        return "\n".join(["".join(map(print_pos, col)) for col in self.area]) + "\n"


area = GuardedArea([[[pos, set()] for pos in row] for row in data[:-1].split("\n")])
print(f"{area.full_movement()}")
# print(area)
