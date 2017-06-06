import sys
import networkx as nx
import bcube.generator_bcube as bcube
import dcell.generate_dcell as dcell
import fat_tree.generate_fat_tree as fatTree
import cayley_graphs.generate_bubble_sort as bubbleSort
import cayley_graphs.generate_hypercube as hypercube

graph_name  = sys.argv[1]
p = int(sys.argv[2])
q = int(sys.argv[3])
path = sys.argv[4]
#integers q, p
#constrains  q < p and q < 4
if graph_name == "bcube":
    G = bcube.generate_bcube(q,p)
elif graph_name == "dcell":
    G = dcell.generate_dcell(q,p)
elif graph_name == "fat_tree":
    #integer p
    #constrains  p must be even
        G = fatTree.generate_fat_tree(p)
elif graph_name == "bubble_sort":
    G = bubbleSort.generate_bubble_sort(p)
elif graph_name == "hypercube":
    G = hypercube.generate_hypercube(p)
edges = G.edges()
H = nx.from_edgelist(edges)
graphml =nx.write_graphml(H, path)

'''
#integers q, p
#constrains  q < p and q < 4
q=3
p=5
path = 'temp/'
dcn_generator("bcube",p,q,path)
q=2
p=3
dcn_generator("dcell",p,q,path)
#cayley
p=6
dcn_generator('bubble_sort',p,q,path)
dcn_generator('hypercube',p,q,path)
#integer k
#constrains  k must be even
dcn_generator('fat_tree',p,q,path)
'''