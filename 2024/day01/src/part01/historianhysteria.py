with open("aoc/2024/day01/resources/data.txt", "r") as file:
    data = file.read()

df = list(
    map(
        list,
        list(
            zip(*list(map(lambda x: map(int, x.split("   ")), data.split("\n")))[:-1])
        ),
    )
)
print(df)

df[0].sort()
df[1].sort()

print(sum([abs(df[0][x] - df[1][x]) for x in range(len(df[0]))]))
