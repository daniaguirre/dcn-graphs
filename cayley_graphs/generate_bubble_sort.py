import networkx as nx
import set_connections as sc

def set_generators(n):
    id = range(0, n)
    #permutation rule
    generators = {}
    for j in range(n-1):
        generator = id[:]
        generator[j] = j+1
        generator[j+1] = j
        generators[j] = generator
    return (id, generators)

def generate_bubble_sort(n):
    G = nx.Graph()
    result = set_generators(n)
    G.graph["name"] = "bubble_sort"
    G.graph["n"] = n
    G.graph["generators"] = result[1]
    G.add_node(tuple(result[0]), id=tuple(result[0]), type='server')
    G = sc.set_connections(G)
    return G