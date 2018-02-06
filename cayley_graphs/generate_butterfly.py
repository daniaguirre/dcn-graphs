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
    return id_bin[::-1]

def get_vertical_node(node, node_id, n, servxlevel, nuSer):
    id_bin = get_binario(node_id[1],n)
    if id_bin[node_id[0]] == 1:
        id_bin[node_id[0]] = 0
    else:
        id_bin[node_id[0]] = 1
    id_dec = 0
    i = 0
    for b in id_bin[::-1]:
        id_dec = id_dec + (b* (2**i) )
        i = i + 1
    pair = (((node_id[0] + 1) * servxlevel) + id_dec)%nuSer
    return pair

def generate_butterfly(n):
    servxlev = 2 ** n
    G = nx.Graph()
    nuSer = servxlev * (n)
    levels = n
    G.add_nodes_from(range(nuSer))
    nx.set_node_attributes(G, 0,'routing_table')
    G.graph['name'] = 'butter'
    G.graph['levels'] = n
    G.graph['servers'] = 2*servxlev
    G.graph['switches'] = (levels-2)*servxlev
    G.graph['parameters'] = {'n': n}

    #labelling and connections
    for node in range(nuSer):
        G.node[node]['id'] = ((node // servxlev), node % servxlev)
        #straight arcs
        straight_arc = (node + servxlev)%nuSer
        G.add_edge(node, straight_arc)
        #vertical arcs
        vertical_arc = get_vertical_node(node, G.node[node]['id'], n, servxlev, nuSer)
        G.add_edge(node, vertical_arc)
        #routing table
        if G.node[node]['routing_table'] == 0:
            G.node[node]['routing_table'] = {}
        if G.node[straight_arc]['routing_table'] == 0:
            G.node[straight_arc]['routing_table'] = {}
        if G.node[vertical_arc]['routing_table'] == 0:
            G.node[vertical_arc]['routing_table'] = {}
        G.node[node]['routing_table'][0] = straight_arc
        G.node[straight_arc]['routing_table'][1] = node
        G.node[node]['routing_table'][2] = vertical_arc
        G.node[vertical_arc]['routing_table'][3] = node
    return G