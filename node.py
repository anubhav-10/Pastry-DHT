import utils
from random import randint
import hashlib

class Node:
	def __init__(self, l = 8):
		b = 4
		self.ip = utils.generate_ip_address()
		self.smaller_leaf_set = [None] * (2 ** (b - 1))
		self.larger_leaf_set = [None] * (2 ** (b - 1))
		self.neighborhood_set = [None] * (2 ** (b + 1))
		self.routing_table = [[None for x in range(2 ** b)] for y in range(l)]

		self.location = [randint(0, 2000), randint(0, 2000)]

		self.node_id = hashlib.md5(self.ip.encode('utf-8')).hexdigest()[:l]

		# for i in range(l):
		# 	self.routing_table[i][int(self.node_id[i], 16)] = self			

	# def print_node(self):
	# 	print (self.ip)
	# 	print ('Node Id: ' + str
	# 		(self.node_id))
	# 	print ('Leaf Set:')
	# 	print (smaller_leaf_set + larger_leaf_set)
	# 	print ()
	# 	print ('Routing Table:')
	# 	for row in self.routing_table:
	# 		print (row)

	# 	print ()
	# 	print ('Neighborhood Set: ' + str(neighborhood_set))
	def print_routing(self):
		print("Routing table. ID: {}".format(self.node_id))
		print()
		print("|" + "-"*(11*16 - 1) + "|")
		# print()
		for x in self.routing_table:
			self.print_arr(x)
			print("|" + "-"*(11*16 - 1) + "|")

	def print_arr(self, arr):
		print("|", end=" ")
		for x in arr:
			if x == None:
				print(x, end="     | ")
			else:
				print(x.node_id, end=" | ")
		print()	
	
	
	def print_node(self):
		print("||||||| --- Printing status of Node with IP: ({}, {}) and Key: {} --- |||||||".format(self.location[0], self.location[1], self.node_id))
		print()
		print("[@] Less Leaf")
		self.print_arr(self.smaller_leaf_set)
		print()

		print("[@] More Leaf")
		self.print_arr(self.larger_leaf_set)

		print()

		print("[@] Neighbor Set")
		print(self.neighborhood_set)

		print()

		# print("[@] Routing Table: ")
		# for x in self.routingTable:
		# self.print_arr(x)
		self.print_routing()
		print()
		print()
		print()