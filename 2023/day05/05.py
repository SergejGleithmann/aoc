with open("aoc/2023/day05/data.txt", "r") as file:
    data = file.read()

with open("aoc/2023/day05/test.txt", "r") as file:
    test = file.read()


def parse_data(data):
    categorys = data.split("\n\n")
    seeds = [int(seed) for seed in categorys[0].strip().split(" ")[1:] if seed != ""]
    return seeds, [
        [[int(num) for num in row.split(" ")] for row in cat.strip().split("\n")[1:]]
        for cat in categorys[1:]
    ]


def translate(seeds, almanach):
    res = []
    for seed in seeds:
        val = seed
        for category in almanach:
            for line in category:
                if line[1] <= val < line[1] + line[2]:
                    val = line[0] + (val - line[1])
                    break
        res.append(val)
    return res


def translate2(seeds, almanach):
    res = []
    for i in range(0, len(seeds), 2):
        print(i / len(seeds) * 2)
        for seed in range(seeds[i], seeds[i] + seeds[i + 1]):
            print(seed)
            val = seed
            for category in almanach:
                for line in category:
                    if line[1] <= val < line[1] + line[2]:
                        val = line[0] + (val - line[1])
                        break
            res.append(val)
    return res


seeds, almanach = parse_data(data)
tseeds, talmanach = parse_data(test)

print(translate(tseeds, talmanach))
print(min(translate(seeds, almanach)))

print(min(translate2(tseeds, talmanach)))
print(min(translate2(seeds, almanach)))
