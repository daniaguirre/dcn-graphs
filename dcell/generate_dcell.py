'''
Program for generate a DCell topology

Required packages:
-networkx

@author: Daniela Aguirre Guerrero
Genera una topologia de red de tipo DCell
RECIBE dos enteros q, p; tales que q < p and q < 4
DEVUELVE un la matriz de adjacency del BCube generado
'''

import networkx as nx
import util_dcell as util

def generate_dcell(q, p):
    G = set_graph_parameters(q, p)
    G = generate_servers(G)
    G = connect_servers(G)
    G = connect_switches(G)
    return G

def set_graph_parameters(n, k):
    '''
    Set graph parameters

    @param n: number of nodes in a DCell0 (recommended value n<=4)
    @param k: k+1 is the number of levels in a DCellK
    @return: a empty graph G (in Networkx format) with params n, k, topology and nxd

    nxd is an array such that nxs[i] is the number of nodes in DCelli
    topology param is DCell
    '''

    G = nx.Graph()
    G.graph['parameters'] = {'k': k, 'n': n}
    G.graph['name'] = 'DCell'

    #Calculates the number of nodes per dcell
    nxd = [n]
    for dcell in range(1, k):
        nxd.append(nxd[-1] * (nxd[-1] + 1))
    G.graph['nxd'] = nxd

    return G

def generate_servers(G):
    '''
    Add servers

    @param G: a returned graph (in Networkx format) by the function set_graph_parameters
    @return: the received graph G (in Networkx format) with param numservs and its server nodes

    Each server nodes has:
     1.- The parameter type with value server
     2.- The param id which is an array such id[i] is the server id in DCelli

    The graph param numservs indicates the numbers of servers that G has
    '''

    #Calculate the among of servers in G
    num_servers = G.graph['nxd'][-1] * ( G.graph['nxd'][-1] + 1 )
    G.add_nodes_from(range(num_servers))
    G.graph['servers'] = num_servers

    #Add server nodes to G
    for node in range(num_servers):
        G.node[node]['type'] = 'server'
        #Set the param id
        G.node[node]['id'] = util.get_array_id(G, node)

    return G

def connect_servers(G):
    '''
    Set connections (edges) between all servers

    @param G: a returned graph (in Networkx format) by the function generate_servers
    @return: the received graph G (in Networkx format) with connections (edges) between its servers
    '''

    nodes = G.nodes()

    #set the connections (edges) for each node
    while len(nodes) > 0:
        node = nodes[0]
        nodes.remove(node)

        #each server connects to k servers
        for connection in range(1, G.graph['parameters']['k']+1):
            #variable connection represent the connection in DCellConnection

            #prefix in DCelli is given by id[k:i]
            #suffix in DCelli is given by uid<i-1>
            prefix = []
            suffix = [G.node[node]['id'][0]]
            for index in range(connection + 1, G.graph['parameters']['k'] + 1):
                prefix.append(G.node[node]['id'][index])
            for index in range(0, connection - 1):
                suffix[0] = suffix[0] + (G.node[node]['id'][index + 1] * G.graph['nxd'][index])
            suffix.append(G.node[node]['id'][connection])

            #according prefix and suffix get the node (pair) to connect
            pair = util.get_pair(G, prefix, suffix)
            if pair in nodes:
                G.add_edge(node, pair)
                if G.degree(pair) == G.graph['parameters']['k']:
                    nodes.remove(pair)

    return G

def connect_switches(G):
    '''
    Add param numswchs to G
    Add node switches to G
    Set connections (edges) between servers and switches

    @param G: a returned graph (in Networkx format) by the function connect_servers
    @return: the received graph G (in Networkx format) with param numswchs and switch nodes and connections (edges) between server and switches

    Each switch node has param type with value switch
    '''

    G.graph['switches'] = G.graph['servers'] / G.graph['parameters']['n']
    G.add_nodes_from(range(G.graph['servers'], G.graph['servers'] + G.graph['switches']))

    #each switch si connected to n servers
    for switch in range(G.graph['switches']):
        G.node[switch + G.graph['servers']]['type'] = 'switch'
        for server in range(switch*G.graph['parameters']['n'], (switch*G.graph['parameters']['n'])+G.graph['parameters']['n']):
            G.add_edge(switch + G.graph['servers'], server)
            G.node[server]['switch'] = switch  + G.graph['servers']

    return G