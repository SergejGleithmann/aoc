with open("aoc/2025/day03/resources/input.txt", "r") as file:
    data = file.read()


with open("aoc/2025/day03/resources/test.txt", "r") as file:
    test = file.read()


def parse(s: str) -> list[list[int]]:
    return [[int(c) for c in line] for line in s.split("\n")]


def max_joltage_1(lst: list[int]) -> int:
    """Solves the first part only by searching fo the two lagest values.

    Args:
        lst (list[int]): battery

    Returns:
        list[int]: max joltage for 2 batteries
    """
    idx_fst, val_fst = max(enumerate(lst), key=lambda x: x[1])
    if idx_fst == len(lst) - 1:
        idx_snd, val_snd = idx_fst, val_fst
        idx_fst, val_fst = max(enumerate(lst[:-1]), key=lambda x: x[1])
    else:
        idx_snd, val_snd = max(enumerate(lst[idx_fst + 1 :]), key=lambda x: x[1])
    return val_fst * 10 + val_snd


def max_joltage(lst: list[int], n: int) -> int:
    """Calculates the max joltage for an arbitrary number of batteries

    Args:
        lst (list[int]): bank
        n (int): number of allowed batteries per bank

    Returns:
        int: maximum joltage
    """

    def extract_numbers(lst: list[int], n: int) -> list[int]:
        """Helper function that returns the subsequence of n batteries with highest joltage.

        Args:
            lst (list[int]): sequence of batteries
            n (int): maximum number of batteries per bank

        Returns:
            list[int]: sequence of n batteries with highest joltage
        """
        if n <= 0:
            return []
        else:
            idx, val = max(enumerate(lst), key=lambda x: x[1])
            right = lst[idx + 1 :]
            if len(right) < n:
                return extract_numbers(lst[:idx], n - len(right) - 1) + [val] + right
            else:
                return [val] + extract_numbers(right, n - 1)

    return int("".join(map(str, extract_numbers(lst, n))))
    # alternative using math
    return sum(
        [x * (10 ** (n - idx - 1)) for idx, x in enumerate(extract_numbers(lst, n))]
    )


# Test cases
print([max_joltage(x, 2) for x in parse(test)])
print([max_joltage(x, 12) for x in parse(test)])

# Full solutions
print(sum([max_joltage(x, 2) for x in parse(data)]))
print(sum([max_joltage(x, 12) for x in parse(data)]))
