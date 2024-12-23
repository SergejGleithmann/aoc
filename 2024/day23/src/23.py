import networkx as nx

with open("aoc/2024/day23/resources/data.txt", "r") as file:
    data = [frozenset(line.strip().split("-")) for line in file.readlines()]
with open("aoc/2024/day23/resources/test.txt", "r") as file:
    test = [frozenset(line.strip().split("-")) for line in file.readlines()]
print(test)


# Naive implementation --- very slow
def get_three_sets(data: list[set[str]]) -> list[set[str]]:
    res = set()
    i = 0
    for g in data:
        print((i * 100) // len(data))
        for h in data:
            if g & h:
                for j in data:
                    if j == g ^ h:
                        res.add(g | h | j)
        i += 1
    return res


def get_adjecency(data: list[set[str]]) -> dict[str, set[str]]:
    graph = {}
    for s in data:
        for e in s:
            graph[e] = (graph.get(e, set()) | s) - {e}
    return graph


def get_three_sets2(data: list[set[str]]) -> list[set[str]]:
    res = set()
    i = 0
    for edge in data:
        x, y = tuple(edge)
        # print((i * 100) // len(data))
        for j in ADJ[x] & ADJ[y]:
            res.add(frozenset((x, y, j)))
        i += 1
    return res


def get_t_sets(lanset: list[set]) -> list[set[str]]:
    res = []
    for s in lanset:
        for x in s:
            if x[0] == "t":
                res.append(s)
                break
    return res


# using networkx
def largest_connection(data: list[set[str]]) -> list[set[str]]:
    g = nx.Graph()
    g.add_edges_from([tuple(d) for d in data])
    len_max = 0
    max_set = set()
    for h in nx.find_cliques(g):
        if len(h) > len_max:
            len_max = len(h)
            max_set = h
    return list(max_set)


# custom implementation
def largest_connection_bk() -> list[set[str]]:
    len_max = 0
    max_set = set()
    for h in bron_kerbosch(set(), set(ADJ.keys()), set()):
        if len(h) > len_max:
            len_max = len(h)
            max_set = h
    return list(max_set)


# custom implementation
def bron_kerbosch(r: set[str], p: set[str], x: set[str]) -> list[set[str]]:
    res = []
    if len(p) == 0 and len(x) == 0:
        return [r]
    else:
        for v in p:
            res.extend(bron_kerbosch(r | {v}, p & ADJ[v], x & ADJ[v]))
            p = p - {v}
            x = x | {v}
    return res


ADJ = get_adjecency(data)

# PART 1
print(len(get_t_sets(get_three_sets2(test))))
print(len(get_t_sets(get_three_sets2(data))))
# PART 2
res = list(largest_connection(test))
res.sort()
print(res)
res = list(largest_connection(data))
res.sort()
print(",".join(res))
res = list(largest_connection_bk())
res.sort()
print(",".join(res))
