#excute permutation
def operation_group(element, generator):
    result = []
    for index in generator:
        result.append(element[index])
    return tuple(result)

#set connections
def set_connections(G):
    nodes = list(G.nodes())
    for node in nodes:
        for generator in G.graph["generators"]:
            pair = operation_group(G.node[node]['id'], G.graph['generators'][generator])
            if not (((node,pair) in G.edges()) or ((pair,node) in G.edges())):
                if not (pair in G.nodes()):
                    G.add_node(pair, type='server', id=pair)
                    nodes.append(pair)
                G.add_edge(node, pair)
    return G