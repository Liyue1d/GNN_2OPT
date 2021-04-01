import pickle
import numpy as np
from numpy import linalg as LA
from scipy.linalg import fractional_matrix_power
import networkx as nx
import xml.etree.ElementTree as ET
import sys

def node_degree(x):
	#Returns the node degree matrix corresponding
	# to the input adjacency matrix x
	# Input: x is a numpy matrix
	# Output: nd_x is a numpy matrix
	size = x.shape[0]
	nd_x = np.matrix(np.zeros((size,size)))
	for i in range(size):
		nd_x[i,i] = np.sum(x[i])
	return nd_x


try:
	root = ET.parse('../input/GRAPH.xml').getroot()

except:
	print("\Fichier XML manquant ou invalide. Placer un fichier graphe GRAPH.xml\
	 valide dans le dossier input.")
	sys.exit()

try:
	vertices_number = root.findall('VERTICES_NUMBER')[0]
	number_of_nodes = int(vertices_number.text)

except:
	print("\n Le nombre de sommets n'est pas indiqué. Se réferer au fichier\
	exemple EXEMPLE.xml ")
	sys.exit()

try:
	adj_matrix = np.zeros((number_of_nodes, number_of_nodes))
	edges_mission = root.findall('EDGES_MISSION')[0]
	for edge in edges_mission:
		source = int(edge.get('src'))
		dest = int(edge.get('dst'))
		distance = float(edge.get('distance'))

		#Recalibrage des indices  0 -> 1 ; Commenter ces deux lignes si on
		#commence depuis 0
		source = source - 1
		dest = dest - 1


		adj_matrix[source, dest] = distance
		print("\n source = %d dest = %d dist = %f "%(source,dest,distance))

except:
	print("\n Format des arrêtes non respecté. Se réferer au fichier\
	exemple EXEMPLE.xml.")
	sys.exit()


print("adj =  \n", adj_matrix)

G = nx.from_numpy_matrix(adj_matrix)
shortest_costs = np.zeros((adj_matrix.shape[0],adj_matrix.shape[0]))
#Number of nodes is stored into variable m_size
m_size = adj_matrix.shape[0]
count = 0

for i in range(adj_matrix.shape[0]):
	for j in range(adj_matrix.shape[0]):
		shortest_costs[i][j] = nx.dijkstra_path_length(G, i, j)
		print("\n %f%%"%(100*count/(adj_matrix.shape[0]*adj_matrix.shape[0])))
		count += 1

a_chap = adj_matrix + np.eye(m_size)
print("achap = \n", a_chap)

d_chap = node_degree(a_chap)
print("dchap \n", d_chap)

inv_sq_root_d_chap = np.matrix(fractional_matrix_power(d_chap, -0.5))
print("inv_sq_root_d_chap =  \n", inv_sq_root_d_chap)
print("(inv_sq_root_d_chap*inv_sq_root_d_chap)^-1 =  \n", LA.inv(inv_sq_root_d_chap*inv_sq_root_d_chap))

sym_norm = inv_sq_root_d_chap * a_chap * inv_sq_root_d_chap
print("sym_norm =  \n", sym_norm)

data = {'adj': adj_matrix, 'prod_matrix': sym_norm, 'number_of_nodes':m_size, 'shortest_costs': shortest_costs}

#Write the data into a pickle file
with open('../model_utils/data.pickle', 'wb') as f:
	# Pickle the 'data' dictionary using the highest protocol available.
	pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
