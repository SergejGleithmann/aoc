from functools import cache
from itertools import permutations


with open("aoc/2024/day21/resources/data.txt", "r") as file:
    data = file.readlines()

codes = [line.strip() for line in data]

NUMPAD: dict[str, complex] = {
    key: x + y * 1j
    for y, line in enumerate(["789", "456", "123", " 0A"])
    for x, key in enumerate(line)
    if key != " "
}
ARRPAD: dict[str, complex] = {
    key: x + y * 1j
    for y, line in enumerate([" ^A", "<v>"])
    for x, key in enumerate(line)
    if key != " "
}
DIRS: dict[str, complex] = {"<": -1 + 0j, "^": -1j, ">": 1 + 0j, "v": 1j}


def vec_to_path(vector: complex):
    return (
        ">" * int(vector.real)
        + "<" * -int(vector.real)
        + "v" * int(vector.imag)
        + "^" * -int(vector.imag)
    )


@cache
def translate_sequence(
    sequence: str, depth: int = 2, arrkey: bool = False, current: complex | None = None
) -> int:
    keys = ARRPAD if arrkey else NUMPAD
    if not sequence:
        return 0
    if not current:
        current = keys["A"]
    next_pos = keys[sequence[0]]

    path_elems = vec_to_path(next_pos - current)
    if depth:
        perm_lens = []
        for perm in set(permutations(path_elems)):
            pos_temp = current
            for button in perm:
                pos_temp += DIRS[button]
                if pos_temp not in keys.values():
                    break
            else:
                perm_lens.append(translate_sequence(perm + ("A",), depth - 1, True))
        min_len = min(perm_lens)
    else:
        min_len = len(path_elems) + 1
    return min_len + translate_sequence(sequence[1:], depth, arrkey, next_pos)


p1 = 0
p2 = 0
for code in codes:
    codenum = int(code[:-1])
    # print(code)
    p1 += codenum * translate_sequence(code)
    p2 += codenum * translate_sequence(code, 25)

print(p1)
print(p2)
