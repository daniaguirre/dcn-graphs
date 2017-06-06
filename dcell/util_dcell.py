__author__ = 'daniela'

def get_array_id(G, node):
    '''
    Get an array id according to received number (node)
    id[i] gives the node position in DCelli

    @param G: a graph (in Networkx format) with all server nodes and params n and k
    @param node: an int that represents de uid in DCell k, for node G.node[node]
    @return: the array id for node G.node[node]
    '''
    id = [node % G.graph['parameters']['n']]
    for index in range(G.graph['parameters']['k']):
        id.append((node % ((G.graph['nxd'][index]+ 1) * G.graph['nxd'][index])) // G.graph['nxd'][index])

    return id

def get_number_id(G, node):
    '''
    Get a number id corresponding to received array (node)

    @param G: a graph (in Networkx format) with all server nodes and params n and k
    @param node: an array that represents de id of a node in G
    @return: the integer of id for node G.node[id]
    '''

    if type(node) is int:
        return node

    id = node[0]
    for index in range(len(node)-1, 0, -1):
        id = id + (node[index] * G.graph['nxd'][index - 1])

    return id

def get_pair(G, prefix, uidk):
    '''
    Given an id (prefix and suffix) for node A, calculates an id for B, in order to connect A to B

    @param G: a graph (in Networkx format)
    @param prefix: in DCelli, it is given by an array [k:i]
    @param suffix: in DCelli, it is given by uid<i-1>
    @return: an integer that represents the node id for connect the node given by received prefix and suffix
    '''
    #i=uidk[1], j-1=uidk[0]
    if (uidk[0] + 1) > uidk[1]:
        pair = [uidk[1], uidk[0] + 1]
    else:
    #i=uidk[0], j=uidk[1]
        pair = [uidk[1]-1, uidk[0]]

    for a in range(len(prefix)):
        pair.append(prefix[a])
    id_pair = pair[0]
    index = -1

    for a in range(len(pair)-1):
        id_pair = id_pair + (pair[index]*G.graph['nxd'][index])
        index -= 1

    return id_pair

def get_comm_prefix(s, t):
    prefix = []
    index = len(s) - 1

    while (index >= 0) and (s[index] == t[index]):
        prefix.append(s[index])
        index -= 1

    suff_s = s[0:len(t) - len(prefix)]
    suff_t = t[0:len(t) - len(prefix)]

    return (prefix, suff_s, suff_t)