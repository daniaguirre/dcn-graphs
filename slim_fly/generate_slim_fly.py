import re
import networkx as nx

def generate_slim_fly(d):
    #regular expressions for reading edges from topology file
    pattern_edge = re.compile('[0-9]+')
    #read topology file
    f = open('slim_fly/edges_format/MMS.'+ str(d) + '.edges.csv','r')
    lines = f.readlines()
    f.close()
    del lines[0]

    edges = []
    for line in lines:
        edge = pattern_edge.findall(line)
        edges.append((int(edge[0]),int(edge[1])))

    G = nx.Graph()
    G.graph['name'] = 'SlimFly'
    G.add_edges_from(edges)

    nx.set_node_attributes(G, 'type', 'server')

    return G