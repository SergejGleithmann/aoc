with open("aoc/2025/day01/resources/input.txt", "r") as file:
    data = file.read()

data = [(-1 if x[0] == "L" else 1) * int(x[1:]) for x in data.split("\n") if len(x) > 0]


def find_zeros(moves: list[int], initial: int = 50) -> tuple[int, int]:
    """Finds the number of times A: the Zero is ended on after a turn or B: the Zero is passed by in total.

    Args:
        moves (list[int]): List of moves, negative numbers mean left, positive right
        initial (int, optional): Initial lock position. Defaults to 50.

        tupel[int,int]: Count of zeros according to method A and B
    """
    position = initial
    zeros_a = 0
    zeros_b = 0
    for move in moves:
        zeros_a += abs((position + move) // 100)
        position = (position + move) % 100
        zeros_b += 1 if (position == 0) else 0
    return zeros_a, zeros_b


print(find_zeros(data))
