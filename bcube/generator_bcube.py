
__name__ = 'generate_topology'

import networkx as nx

"""Genera una topologia de red de tipo BCube"""

"""RECIBE el parametro k que debe ser un numero >= 1 y el parametro n
DEVUELVE un grafo de nx"""

def generate_servers(n, k):
    G = nx.Graph()
    G.graph['parameters'] = {'k':k, 'n':n}
    G.graph['servers'] = n**(k+1)
    G.add_nodes_from(range(G.graph['servers']))
    for node in range(G.graph['servers']):
        G.node[node]['type'] = 'server'
    return G

def connect_levels(G):
    switches_per_level = G.graph['parameters']['n'] ** G.graph['parameters']['k']
    G.graph['switches'] = (G.graph['parameters']['k']+1) * switches_per_level
    for level in range(G.graph['parameters']['k']+1):
        switches = range(G.graph['servers'] + (level*switches_per_level), G.graph['servers'] + (level*switches_per_level) + switches_per_level)
        G.add_nodes_from(switches)
        for switch in range(G.graph['servers'] + (level*switches_per_level), G.graph['servers'] + (level*switches_per_level) + switches_per_level):
            G.node[switch]['type'] = 'switch'
            G.node[switch]['level'] = level
        switch_ini = 0
        for bcubek in range (G.graph['parameters']['n']**(G.graph['parameters']['k']-level)):
            server_ini = bcubek*G.graph['parameters']['n']**(level+1)
            for switch in range(G.graph['parameters']['n']**level):
                for server in range(server_ini, server_ini + G.graph['parameters']['n']**(level+1), G.graph['parameters']['n']**level):
                    G.add_edge(server, switches[switch_ini])
                server_ini+=1
                switch_ini+=1
    return G

def generate_bcube(q, p):
    G = generate_servers(q, p)
    G = connect_levels(G)
    G.graph['name'] = "BCube"
    A = nx.adjacency_matrix(G)
    return A