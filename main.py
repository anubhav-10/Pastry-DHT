import node
import utils

nodes = []
l = 32
b = 4

def add_node(X):
	A = utils.get_closest_node(nodes, X)

	if (A == None):
		print ('First Node')
		nodes.append(X)
		return

	utils.update_neighborhood_set(X, A)
	utils.update_routing_table(X, A)

	for i in range(l):
		X.routing_table[i][int(X.node_id[i], 16)] = X			

	