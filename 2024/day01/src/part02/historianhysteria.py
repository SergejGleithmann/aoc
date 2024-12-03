from typing import Dict, List


with open("aoc/2024/day01/resources/data.txt", "r") as file:
    data = file.read()

df = map(
    list,
    list(zip(*list(map(lambda x: map(int, x.split("   ")), data.split("\n")))[:-1])),
)


def get_occ_dict(l: List[int]) -> Dict[int, int]:
    occs: Dict[int, int] = {}
    for x in l:
        occs[x] = occs.get(x, 0) + 1
    return occs


def similarity(l1: List[int], l2: List[int]) -> int:
    a = get_occ_dict(l1)
    b = get_occ_dict(l2)
    res = 0
    for k, v in a.items():
        res += k * b.get(k, 0) * v
    return res


print(similarity(*df))
