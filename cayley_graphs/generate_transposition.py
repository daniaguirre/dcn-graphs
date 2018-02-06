import networkx as nx
import set_connections as sc

#set connections and id's
def set_generators(n):
    id = range(0, n)
    #permutation rule
    generators = {}
    for i in id:
        for j in range(i+1, n):
            generator = id[:]
            generator[i] = j
            generator[j] = i
            generators[(i,j)] = generator

    return (id, generators)

def generate_transposition_graph(n):
    G = nx.Graph()
    result = set_generators(n)
    G.graph["name"] = "transposition_graph"
    G.graph["n"] = n
    G.graph["generators"] = result[1]
    G.add_node(tuple(result[0]), id= tuple(result[0]), type= 'server')
    G = sc.set_connections(G)
    return G