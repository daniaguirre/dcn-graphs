import sys
import networkx as nx
import bcube.generator_bcube as bcube
import dcell.generate_dcell as dcell
import fat_tree.generate_fat_tree as fatTree
import cayley_graphs.generate_bubble_sort as bubbleSort
import cayley_graphs.generate_hypercube as hypercube
import cayley_graphs.generate_pancake as pancake
import cayley_graphs.generate_transposition as transposition
import cayley_graphs.generate_star as star
import cayley_graphs.generate_butterfly as butterfly
import slim_fly.generate_slim_fly as slimFly

graph_name  = sys.argv[1]
p = int(sys.argv[2])
q = int(sys.argv[3])
path = 'temp/' + sys.argv[4]
#integers q, p
if graph_name == "bcube":
    #constrains  q < p and q < 4
    G = bcube.generate_bcube(q,p)
elif graph_name == "dcell":
    #constrains  q < p and q < 4
    G = dcell.generate_dcell(p,q)
elif graph_name == "fat_tree":
    #integer p
    #constrains  p must be even
    G = fatTree.generate_fat_tree(p)
elif graph_name == "bubble_sort":
    G = bubbleSort.generate_bubble_sort(p)
elif graph_name == "hypercube":
    G = hypercube.generate_hypercube(p)
elif graph_name == "pancake":
    G = pancake.generate_pancake_graph(p)
elif graph_name == "transposition":
    G = transposition.generate_transposition_graph(p)
elif graph_name == "star":
    G = star.generate_star_graph(p)
elif graph_name == "butterfly":
    G = butterfly.generate_butterfly(p)
elif graph_name == "slim_fly":
    # p = 5,7,11,17,19,25,29,35,43,47,55,79
    G = slimFly.generate_slim_fly(p)

edges = G.edges()
#print G.nodes(data=True)
H = nx.from_edgelist(edges)
#changing color of nodes
#H.node[1]['co']='red'
nodes = len(H.nodes(data=True))
print nodes
nx.write_graphml(H, path + str(nodes))