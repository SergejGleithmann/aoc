from functools import cache, lru_cache
import sys

sys.setrecursionlimit(3000)

type delta = tuple[int, int, int, int]

with open("aoc/2024/day22/resources/data.txt", "r") as file:
    data = [int(line.strip()) for line in file.readlines()]


test = [1, 10, 100, 2024]
test_res = [8685429, 4700978, 15273692, 8667524]


def prune(x: int) -> int:
    return x % 16777216


def derive(x: int) -> int:
    x = prune(x ^ (x << 6))
    x = prune(x ^ (x >> 5))
    x = prune(x ^ (x << 11))
    return x


# @cache
# @lru_cache(maxsize=None)
def derive_n(x: int, n: int) -> list[int]:
    if n == 0:
        return [x]
    else:
        return [x] + derive_n(derive(x), n - 1)


def rand_to_price(rand_seq: list[int]) -> int:
    return [p % 10 for p in rand_seq]


def price_list(rand_seq: list[int]) -> dict[delta, int]:
    price_seq = rand_to_price(rand_seq)
    seq_to_banana = {}
    diff = tuple(map(lambda x, y: x - y, price_seq[1:], price_seq[:-1]))
    for i in range(4, len(price_seq)):
        seq_to_banana.setdefault(diff[i - 4 : i], price_seq[i])
    return seq_to_banana


def merge_banana_dicts(banana_dicts: list[dict[delta, int]]) -> dict[delta, int]:
    total = {}
    for d in banana_dicts:
        # print("d", d.get((-2, 1, -1, 3), None))
        # print("t", total.get((-2, 1, -1, 3), None))
        for k, v in d.items():
            total[k] = total.get(k, 0) + v
    return total


def max_bananas(total: dict[delta, int]) -> tuple[delta, int]:
    v_max = 0
    k_max = None
    for k, v in total.items():
        if v > v_max:
            k_max = k
            v_max = v
    return k_max, v_max


for x, r in zip(test, test_res):
    res = derive_n(x, 2000)
    # print(price_list(res))
    assert res[-1] == r
    print(f"{x}: {res[-1]}")

# data = [1, 2, 3, 2024]
ITERATIONS = 2000
prices = [derive_n(x, ITERATIONS) for x in data]

print(
    f"Part 1: Sum of Sequence at position {ITERATIONS} is {sum([p[-1] for p in prices])}"
)

bananas = [price_list(p) for p in prices]

total = merge_banana_dicts(bananas)

k_max, v_max = max_bananas(total)
print(f"Part 2: Best sequence is {k_max} with {v_max} total bananas.")
