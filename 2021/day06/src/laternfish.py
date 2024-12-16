with open("aoc/2021/day06/resources/data.txt", "r") as file:
    data = file.read()

fish = [int(n) for n in data.strip().split(",") if n in "0123456789"]
print(len(fish))
cache = {}


def iteration(fish: int, iterations: int):
    if iterations == 0:
        res = 1
    elif (fish, iterations) in cache.keys():
        return cache[(fish, iterations)]
    elif fish == 0:
        res = iteration(6, iterations - 1) + iteration(8, iterations - 1)
    else:
        res = iteration(fish - 1, iterations - 1)
    cache[(fish, iterations)] = res
    return res


def iteration2(fishes):
    for i in range(len(fishes)):
        if fishes[i] > 0:
            fishes[i] -= 1
        elif fishes[i] == 0:
            fishes[i] = 6
            fishes.append(8)


ITER = 256
# fish = [3, 4, 3, 1, 2]
print(sum([iteration(f, ITER) for f in fish]))
""" for i in range(ITER):
    iteration2(fish)
print(len(fish)) """
