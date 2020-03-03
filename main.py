from node import Node
import utils
import sys

nodes = []
l = 8
b = 4

def add_node(X):
	A = utils.get_closest_node(nodes, X)
	if (A == None):
		print ('First Node')
		nodes.append(X)
		for i in range(l):
			X.routing_table[i][int(X.node_id[i], 16)] = X
		return

	print(A.node_id, X.node_id)
	nodes.append(X)
	utils.update_neighborhood_set(X, A)
	utils.update_routing_table(X, A)

	for i in range(l):
		X.routing_table[i][int(X.node_id[i], 16)] = X

	utils.update_others(X)		

def remove_node(X):
	utils.remove_node(nodes, X)

num = int(sys.argv[1])
for i in range(num):
	new_node = Node()
	add_node(new_node)

for node in nodes:
	node.print_node()