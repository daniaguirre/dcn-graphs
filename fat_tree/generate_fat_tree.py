import networkx as nx

"""Genera una topologia de red de tipo Fat-Tree"""

"""RECIBE el parametro k que debe ser un numero par > 2
DEVUELVE un grafo de nx en donde cada nodo tiene un parametro type"""

"""El parametro type puede tener uno de los siguientes valores:
 1)core, 2)aggregation, 3)edge y 4)host"""

def generate_fat_tree(k):

    #numeros de cores y de switches por capa

     #numero de switch por capa

    # create networkx graph with total number of nodes
    G = nx.Graph()
    G.graph['parameters'] = {'k': k}
    G.graph['nuCor'] = (k/2)**2 #numero de cores
    G.graph['nuSwl'] = k**2/2  #numero de switch por capa (edge, aggregation)
    G.graph['nuServ'] = 9 * (k**2) / 4
    G.graph['switches'] = G.graph['nuCor'] + (2*(G.graph['nuSwl']))
    G.graph['servers'] = k**3/4
    G.graph['name'] = 'Fat-Tree'
    # Se agrega la cantidad total de nodos
    G.add_nodes_from(range(9*k**2 / 4))

    #Ids iniciales de los cores, switches y host
    idCor = range(G.graph['nuCor'])
    idASw = range(idCor[-1] + 1, G.graph['nuSwl']  + G.graph['nuCor'])
    idESw = range(idASw[-1] + 1, 2*G.graph['nuSwl'] + G.graph['nuCor'])
    idHos = range(idESw[-1] + 1, idESw[-1] + G.graph['servers'] + 1)

    #Se agregan los enlaces
    for inSwi in range(0,G.graph['nuSwl']):
        #Enlaces entre los aggregation switches y los cores
        fsCor = (inSwi % (k/2)) * k/2
        for inCor in range(fsCor, fsCor + k/2):
            G.add_edge(idASw[inSwi], idCor[inCor])
        #Enlaces entre los aggregation switches y los edge switches
        fsESw = (inSwi // (k/2)) * k/2
        for inESw in range(fsESw, fsESw + k/2):
            G.add_edge(idASw[inSwi], idESw[inESw])
        #Enlaces entre los edge switches y los host
        fsHos = inSwi * (k/2)
        for inHos in range(fsHos, fsHos + k/2):
            G.add_edge(idESw[inSwi], idHos[inHos])

    #Agregamos el parametro type como dato de cada nodo
    G.add_nodes_from(idCor, type="core")
    G.add_nodes_from(idASw, type="aggregation")
    G.add_nodes_from(idESw, type="edge")
    G.add_nodes_from(idHos, type="server")

    #Marcamos a los aggregation y edge switchs con su numero de core
    for pod in range(k):
        G.add_nodes_from(range(G.graph['nuCor'] + pod*k/2, G.graph['nuCor'] + (k/2) + pod*k/2), pod = pod)
        G.add_nodes_from(range(G.graph['nuCor'] + G.graph['nuSwl'] + pod*k/2, G.graph['nuCor'] + (k/2) + G.graph['nuSwl'] + pod*k/2), pod = pod)

    return G