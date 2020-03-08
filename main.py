from node import Node
import utils
import sys
import random
from collections import Counter

nodes = []
keys = []
hash_table = {} 
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

	# print(A.node_id, X.node_id)
	nodes.append(X)
	utils.update_neighborhood_set(X, A)
	utils.update_routing_table(X, A)

	for i in range(l):
		X.routing_table[i][int(X.node_id[i], 16)] = X

	utils.update_others(X)		

def route_msg(data = None, key = None):
	if key == None:
		key = hex(random.randint(0, 2**(b*l) - 1))[2:]
		key = '0' * (l - len(key)) + key
	if data == None:
		data = hex(random.randint(0, 2**(b*l) - 1))[2:]
		
	random_node = random.choice(nodes)
	utils.route_msg(random_node, key, data)
	keys.append(key)
	# hash_table[key] = data

def route_multiple_msg(num):
	for i in range(num):
		route_msg()

def check_msg_route():
	error = 0
	for i in hash_table:
		if hash_table[i] != get_msg(i)[0]:
			error += 1

	print (error)

def get_msg(key):
	random_node = random.choice(nodes)
	data, hops = utils.get_msg(random_node, key)
	return data, hops

def remove_node(X):
	utils.remove_node(nodes, X)
	nodes.remove(X)

def remove_random_node():
	random_node = random.choice(nodes)
	remove_node(random_node)

def add_multiple_nodes(num):
	for i in range(num):
		new_node = Node()
		add_node(new_node)

def remove_multiple_nodes(num):
	for i in range(num):
		remove_random_node()
		print ("Deleted: " + str(i))

def print_all_nodes():
	for node in nodes:
		node.print_node()	

def reset():
	nodes = []
	keys = []
