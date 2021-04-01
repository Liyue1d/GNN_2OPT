import sys
sys.path.insert(0, 'src/')
from TwoOptClient import twoOptCompute
import numpy as np

import csv
import pickle
# Load the graph data
with open('../model_utils/data.pickle', 'rb') as f:
	data = pickle.load(f)

# Store graph data into variables
A = data.get('adj')
shortest_costs = data.get('shortest_costs')
number_of_nodes = data.get('number_of_nodes')
number_of_features_per_node = 3
x_size = number_of_nodes * number_of_features_per_node
y_size = number_of_nodes

exec(open("./pi.py").read())

start = int(sys.argv[1])
end = int(sys.argv[2])
mandatory = list(map(int,sys.argv[3].split(",")))


instance = [start, end, mandatory]
nv = instance.copy()
nv[2] = instance[2].copy()
gcn_order = pi(nv)
order_inst = instance.copy()
order_inst[2] = gcn_order.copy()



#with init
order_results = twoOptCompute(A,order_inst)
order_path = order_results[0]
order_solution_cost = order_results[1]
order_mand_order_int = order_results[2]
order_attempts = order_results[3]
order_swap_cnt = order_results[4]
order_permutation_group = order_results[5]
order_compute_time = float(order_results[6])
order_score_value = order_results[7]

print("\nOrder suggested by GCN: %s"%gcn_order)

print("Order of visit of mandatory nodes with init: %s"%order_mand_order_int)

print("Solution path with init: %s"%order_path)

print("Cost of solution path with init: %.2f "%order_solution_cost)

print("Number of attempted swaps with init: %d "%order_attempts)

print("Number of swaps with init: %d \n"%order_swap_cnt)

print("permutation_group with init: %s \n"%order_permutation_group)

print("compute time with init: %f \n"%order_compute_time)

file = open("results.txt","w")

file.write("%s\n"% ",".join(list(map(str, order_path))))
file.write("%f\n"%order_solution_cost)
file.write("%s\n"%",".join(list(map(str, order_mand_order_int))))
file.write("%f\n"% order_compute_time)

file.close()

sess.close()
tf.reset_default_graph()
