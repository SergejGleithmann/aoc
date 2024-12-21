# import numpy as np
from functools import cache


with open("aoc/2024/day21/resources/data.txt", "r") as file:
    data = file.readlines()

""" with open("aoc/2024/day21/resources/test.txt", "r") as file:
    data = file.readlines() """

N = {str(i + 1): i % 3 + 1 + (i // 3) * 1j + 1j for i in range(9)}
N["0"] = 2 + 0j
N["A"] = 3 + 0j
N[" "] = 1 + 0j

A = {
    "<": 1 + 0j,
    "v": 2 + 0j,
    ">": 3 + 0j,
    " ": 1 + 1j,
    "^": 2 + 1j,
    "A": 3 + 1j,
}
pos_to_a = {v: k for k, v in A.items()}

d_to_v = {"^": 1j, ">": 1 + 0j, "v": -1j, "<": -1 + 0j}


def v_to_steps(v, vertical: bool):
    horizontal_moves = ("<" if v.real < 0 else ">") * int(abs(v.real))
    vertical_moves = ("v" if v.imag < 0 else "^") * int(abs(v.imag))
    if vertical:
        return vertical_moves + horizontal_moves + "A"
    else:
        return horizontal_moves + vertical_moves + "A"


# print(n_to_pos)


@cache
def path(start, dest, last=False) -> list[int]:
    pad = N if (start in N and dest in N) else A
    print(start, dest, last, pad)
    v = pad[dest] - pad[start]
    return v_to_steps(v, pad[" "] == pad[start] + v.real)


@cache
def length(code, depth, s=0, start=True):
    if depth == 0:
        return len(code)
    for i, c in enumerate(code):
        print(depth)
        p = path(code[i - 1], c, start)
        s += length(p, depth - 1, False)
    return s


def solve_crosspad(code):
    pos = A["A"]
    res = []
    for c in code:
        if c == "A":
            res.append(pos_to_a[pos])
        else:
            pos += d_to_v[c]
    return res


""" print("".join(numpad("029A")))
d = n_to_pos["2"] - n_to_pos["0"]
print(d)
print(v_to_steps(d)) """

print("".join("029A"))


def complexity(code, depth):
    path.cache_clear()
    length.cache_clear()
    # print(len(crosspad(crosspad(numpad(code)))), int(code[:-1]))
    return length(code, depth, True) * int(code[:-1])


print(sum([complexity(code.strip(), 3) for code in data]))

""" print(
    sum([complexity(code.strip()) for code in ["029A", "980A", "179A", "456A", "379A"]])
)
print("".join(crosspad(crosspad(numpad("456A")))))
print("".join(solve_crosspad(solve_crosspad(crosspad(crosspad(numpad("456A"))))))) """
