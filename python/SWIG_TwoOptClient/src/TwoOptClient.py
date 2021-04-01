#!/usr/bin/python
import sys
import numpy as np
import networkx as nx
import time

sys.path.append('lib')
from TwoOpt import *

import pickle
# Load the graph data
with open('../model_utils/data.pickle', 'rb') as f:
	data = pickle.load(f)

shortest_costs = data.get('shortest_costs')

def twoOptCompute(A,instance):

	n = A.shape[0]
	G = nx.from_numpy_matrix(A)

	#Instance to solve
	departure = instance[0]
	arrival = instance[1]
	mandatories = instance[2]
	mand_order = np.array(mandatories).astype(float)

	#Nodes of new graph
	new_nodes = []
	new_nodes.append(departure)
	new_nodes.append(arrival)
	new_nodes.extend(mandatories)
	ngs = len(new_nodes)
	#Solver instanciation and run
	solver = TwoOpt()
	inf = np.array([0.,0., 0.])
	permutation_group = np.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
	score_value = np.zeros(100)
	start_time = time.time()
	solver.optimize(mand_order, shortest_costs, departure, arrival, inf, permutation_group, score_value)
	compute_time = time.time() - start_time
	mand_order_int = mand_order.astype(int)
	solution_cost = inf[0]
	swap_cnt = int(inf[1])
	attempts = int(inf[2])

	#Path rebuilding
	path = []
	path.extend(nx.dijkstra_path(G, departure, mand_order_int[0]));
	for i in range(mand_order_int.size - 1):
		sp = nx.dijkstra_path(G,mand_order_int[i], mand_order_int[i+1])
		del(sp[0])
		path.extend(sp)
	sp = nx.dijkstra_path(G, mand_order_int[-1], arrival)
	del(sp[0])
	path.extend(sp)

	#Output

	return [path, solution_cost, mand_order_int, attempts, swap_cnt, permutation_group, compute_time, score_value]
