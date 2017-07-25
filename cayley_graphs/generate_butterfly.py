import networkx as nx

def get_binario(id, d):
    id_bin = []
    res = id
    for zero in range(d):
        id_bin.append(0)
    index = 0
    while res!=0:
        id_bin[index] = res % 2
        res = res // 2
        index += 1
    return id_bin

def get_vertical_node(node, n, servxlevel):
    id=node[0]
    id_bin = get_binario(id, n)
    pair = servxlevel * node[1]

    if id_bin[node[1] - 1] == 0:
        id_bin[node[1] - 1] = 1
    else:
        id_bin[node[1] - 1] = 0

    base = 1

    for value in id_bin:
        pair = pair + (base*value)
        base = base * 2

    return pair

def generate_butterfly(n):
    servxlev = 2 ** n
    G = nx.Graph()
    nuSer = servxlev * (n+1)
    levels = n + 1
    G.add_nodes_from(range(nuSer))
    G.graph['name'] = 'butter'
    G.graph['levels'] = n + 1
    G.graph['servers'] = 2*servxlev
    G.graph['switches'] = (levels-2)*servxlev
    G.graph['parameters'] = {'n': n}

    #labelling and connections
    for node in range(nuSer):
        G.node[node]['id'] = (node % servxlev, (node // servxlev) + 1 )
        G.node[node]['routing_table'] = {}
        #next neighbors
        if node < servxlev*(levels-1):
            #straight arcs
            straight_arc = node + servxlev
            G.add_edge(node, straight_arc)
            #vertical arcs
            vertical_arc = get_vertical_node( G.node[node]['id'],n,servxlev)
            G.add_edge(node, vertical_arc)
            #routing table
            G.node[node]['routing_table'][0] = straight_arc
            G.node[node]['routing_table'][2] = vertical_arc
        #back neighbors
        if node >= servxlev:
            G.node[node]['routing_table'][1] = node-servxlev
            for neighbor in G.neighbors(node):
                if (neighbor < node) and (neighbor != (node-servxlev)):
                    G.node[node]['routing_table'][3] = neighbor
    return G