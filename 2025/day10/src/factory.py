from queue import Queue
from z3 import Int, Optimize


def parse(s: str) -> dict[str, list[bool] | list[int]]:
    splitted = s.strip().split(" ")
    return {
        "goal": [c == "#" for c in splitted[0][1:-1]],
        "buttons": [[int(x) for x in btn[1:-1].split(",")] for btn in splitted[1:-1]],
        "joltage": [int(x) for x in splitted[-1][1:-1].split(",")],
    }


with open("aoc/2025/day10/resources/input.txt", "r") as file:
    data = [parse(line) for line in file.readlines()]


with open("aoc/2025/day10/resources/test.txt", "r") as file:
    test = [parse(line) for line in file.readlines()]


def toggle_btn(state: list[bool], btn: list[int]) -> list[bool]:
    return [x ^ (i in btn) for i, x in enumerate(state)]


def switch_on(problem: dict[str, list[bool] | list[int]]) -> int:
    state = [False] * len(problem["goal"])
    queue = Queue()
    queue.put((state, 0, []))
    while True:
        state, n, moves = queue.get()
        for btn in problem["buttons"]:
            next_state = toggle_btn(state, btn)
            if next_state == problem["goal"]:
                return n + 1
            else:
                queue.put((next_state, n + 1, moves + [btn]))


def solve_joltage(problem: dict[str, list[bool] | list[int]]) -> int:
    presses = Int("presses")
    btn_presses = [Int(f"Press{i}") for i in range(len(problem["buttons"]))]
    # out_val = [Int(f"Out{i}") for i in range(len(problem["joltage"]))]
    equations = [presses == sum(btn_presses)]
    for i, t in enumerate(problem["joltage"]):
        equations.append(
            t
            == sum(
                [btn for j, btn in enumerate(btn_presses) if i in problem["buttons"][j]]
            )
        )
    for btn in btn_presses:
        equations.append(btn >= 0)

    opt = Optimize()
    opt.add(equations)
    opt.minimize(presses)
    opt.check()
    return int(str(opt.model()[presses]))


print(sum([switch_on(p) for p in test]))
print(sum([switch_on(p) for p in data]))

print(sum([solve_joltage(p) for p in test]))
print(sum([solve_joltage(p) for p in data]))
