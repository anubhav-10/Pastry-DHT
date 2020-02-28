import random
import math
import os
import itertools

def generate_ip_address():
	return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

def euclidean_distance(x, y):
	return sqrt((x.location[1] - y.location[1]) ** 2 + (x.location[0] - y.location[1]) ** 2)

def get_closest_node(nodes, X):
	closest_node = None
	min_dist = math.inf
	for node in nodes:
		dist = euclidean_distance(X, node)
		if dist < min_dist:
			min_dist = dist
			closest_node = node

	return closest_node

def update_neighborhood_set(X, A):
	X.neighborhood_set = [x for x in  A.neighborhood_set]
	max_dist = -1 * math.inf
	max_index = -1
	for index, node in enumerate(X.neighborhood_set):
		if node == None:
			X.neighborhood_set[index] = A
			return

		dist = euclidean_distance(X, node)
		if dist > max_dist:
			max_dist = dist
			max_index = index

	X.neighborhood_set[max_index] = A

def update_routing_table(X, A):
	# while (1):
	l = shl(X.node_id, A.node_id)
	X.routing_table[l] = [x for x in A.routing_table[l]]

	min_A_leaf_set, ind = get_min_leaf_set(A)
	max_A_leaf_set, ind = get_max_leaf_set(A)

	if not min_A_leaf_set:
		min_A_leaf_set = A
	if not max_A_leaf_set:
		max_A_leaf_set = A

	if min_A_leaf_set.node_id <= X.node_id <= max_A_leaf_set.node_id:
		closest_node = get_closest_node_leaf_set(X, A)
		if get_key_distance(X, A) < get_key_distance(X, closest_node):
			update_leaf_set(X, A)
			return
	else:
		l = shl(X.node_id, A.node_id)
		B = A.routing_table[l][int(X.node_id[l], 16)]
		if B:
			update_routing_table(X, B)
		else:
			T_set = A.neighborhood_set + A.smaller_leaf_set + A.larger_leaf_set
			flatten_routing_table = list(itertools.chain.from_iterable(A.routing_table))
			T_set += flatten_routing_table
			T_set = set(T_set)
			T_set.discard(None)

			for t in T_set:
				if shl(t.node_id, X.node_id) >= l and get_key_distance(t, X) < get_key_distance(A, X):
					update_routing_table(X, t)
					break
			else:
				update_leaf_set(X, A)
				return

def update_others(X):
	T_set = X.neighborhood_set + X.smaller_leaf_set + X.larger_leaf_set
	flatten_routing_table = list(itertools.chain.from_iterable(X.routing_table))
	T_set += flatten_routing_table
	T_set = set(T_set)
	T_set.discard(None)

	for t in T_set:
		if X.node_id < t.node_id:
			min_node, min_index = get_min_leaf_set(t)
			t.smaller_leaf_set[min_index] = X

		if X.node_id > t.node_id:
			max_node, max_index = get_max_leaf_set(t)
			t.larger_leaf_set[max_index] = X

		l = shl(X.node_id, t.node_id)
		if not t.routing_table[l][int(X.node_id[l], 16)]:
			t.routing_table[l][int(X.node_id[l], 16)] = X

		max_dist = -1 * math.inf
		max_index = -1
		for index, node in enumerate(t.neighborhood_set):
			if node == None:
				t.neighborhood_set[index] = X
				break

			dist = euclidean_distance(t, node)
			if dist > max_dist:
				max_dist = dist
				max_index = index
		else:
			if euclidean_distance(X, t) < max_dist:
				t.neighborhood_set[max_index] = X

def update_leaf_set(X, Z):
	X.smaller_leaf_set = [x for x in Z.smaller_leaf_set]
	X.larger_leaf_set = [x for x in Z.larger_leaf_set]

	if Z.node_id < X.node_id:
		min_node, min_index = get_min_leaf_set(Z)
		X.smaller_leaf_set[min_index] = Z

	if Z.node_id > X.node_id:
		max_node, max_index = get_max_leaf_set(Z)
		X.larger_leaf_set[max_index] = Z

def shl(x, y):
	l = [x, y]
	return len(os.path.commonprefix(l))

def get_min_leaf_set(A):
	min_node = None
	min_index = -1
	for index, node in enumerate(A.smaller_leaf_set):
		if node:
			if not min_node:
				min_node = node:
				min_index = index
			elif min_node > node:
				min_node = node
				min_index = index

	return min_node, min_index

def get_max_leaf_set(A):
	max_node = None
	max_index = -1
	for index, node in enumerate(A.larger_leaf_set):
		if node:
			if not max_node:
				max_node = node:
				max_index = index
			elif max_node < node:
				max_node = node
				max_index = index

	return max_node, max_index

def get_closest_node_leaf_set(X, A):
	closest_node = None
	min_dist = math.inf

	for node in A.smaller_leaf_set + A.larger_leaf_set:
		if node:
			dist = get_key_distance(X, node)
			if dist < min_dist:
				min_dist = dist
				closest_node = node

	return node

def get_key_distance(a, b):
	return abs(int(a.node_id, 16) - int(b.node_id, 16))