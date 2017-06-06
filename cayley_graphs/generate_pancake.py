import networkx as nx
from symm_cayley.util import set_connections as sc

def set_generators(n):
    id = range(0, n)
    #permutation rule
    generators = {}
    for j in range(1, n):
        generator = range(j,-1,-1)
        generator[j+1:n] = range(j+1,n)
        generators[j] = generator
    return (id, generators)

def generate_pancake_graph(n):
    G = nx.Graph()
    result = set_generators(n)
    G.graph["name"] = "pancake_graph"
    G.graph["n"] = n
    G.graph["generators"] = result[1]
    G.add_node(tuple(result[0]), {'id': tuple(result[0]), 'type': 'server'})
    G = sc.set_connections(G)
    return G