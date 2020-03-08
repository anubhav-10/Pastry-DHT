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
		self.hash_table = {}
		# for i in range(l):
		# 	self.routing_table[i][int(self.node_id[i], 16)] = self			

	def print_node(self):
		print (self.ip)
		print ('Node Id: ' + str
			(self.node_id))
		print ('Leaf Set:')
		print (self.smaller_leaf_set + self.larger_leaf_set)
		print ()
		print ('Routing Table:')
		for row in self.routing_table:
			print (row)

		print ()
		print ('Neighborhood Set: ' + str(self.neighborhood_set))
