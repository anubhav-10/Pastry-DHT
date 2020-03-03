import random
from math import sqrt
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

	if not min_A_leaf_set and not max_A_leaf_set:
		update_leaf_set(X, A)
		return

	if not min_A_leaf_set:
		min_A_leaf_set = A
	if not max_A_leaf_set:
		max_A_leaf_set = A

	if min_A_leaf_set.node_id <= X.node_id <= max_A_leaf_set.node_id:
		closest_node = get_closest_node_leaf_set(X, A)
		if closest_node == A:
			update_leaf_set(X, A)
			return
		else:
			update_routing_table(X, closest_node)
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
			T_set.discard(A)
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
	T_set.discard(X)

	for t in T_set:
		if X.node_id < t.node_id:
			if None in t.smaller_leaf_set:
				none_index = t.smaller_leaf_set.index(None)
				t.smaller_leaf_set[none_index] = X
			else:
				min_node, min_index = get_min_leaf_set(t)
				if min_node.node_id < X.node_id:
					t.smaller_leaf_set[min_index] = X

		if X.node_id > t.node_id:
			if None in t.larger_leaf_set:
				none_index = t.larger_leaf_set.index(None)
				t.larger_leaf_set[none_index] = X
			else:
				max_node, max_index = get_max_leaf_set(t)
				if max_node.node_id > X.node_id:
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
		if None in X.smaller_leaf_set:
			none_index = X.smaller_leaf_set.index(None)
			X.smaller_leaf_set[none_index] = Z
		else:
			min_node, min_index = get_min_leaf_set(Z)
			if get_key_distance(Z, X) < get_key_distance(min_node, X):
				X.smaller_leaf_set[min_index] = Z

	if Z.node_id > X.node_id:
		if None in X.larger_leaf_set:
			none_index = X.larger_leaf_set.index(None)
			X.larger_leaf_set[none_index] = Z
		else:
			max_node, max_index = get_max_leaf_set(Z)
			if get_key_distance(Z, X) < get_key_distance(max_node, X):
				X.larger_leaf_set[max_index] = Z

def remove_node(nodes, X):
	for node in nodes:
		# Repair leaf set
		if X in node.larger_leaf_set:
			X_index = node.larger_leaf_set.index(X)
			node.larger_leaf_set[X_index] = None

			max_node, max_index = get_max_leaf_set(node)
			if max_node:
				leaf_set = max_node.smaller_leaf_set + max_node.larger_leaf_set
				eligible_leaf = []
				for leaf in leaf_set:
					if leaf not in node.larger_leaf_set and leaf != node and leaf.node_id > node.node_id:
						eligible_leaf.append(leaf)
				closest_node = get_closest_node_wrt_key(eligible_leaf, node)
				node.larger_leaf_set[X_index] = closest_node

		elif X in node.smaller_leaf_set:
			X_index = node.smaller_leaf_set.index(X)
			node.smaller_leaf_set[X_index] = None

			min_node, min_index = get_min_leaf_set(node)
			if min_node:
				leaf_set = min_node.smaller_leaf_set + min_node.larger_leaf_set
				eligible_leaf = []
				for leaf in leaf_set:
					if leaf not in node.smaller_leaf_set and leaf != node and leaf.node_id < node.node_id:
						eligible_leaf.append(leaf)
				closest_node = get_closest_node_wrt_key(eligible_leaf, node)
				node.smaller_leaf_set[X_index] = closest_node

		# Repair neighborhood set
		if X in node.neighborhood_set:
			X_index = node.neighborhood_set.index(X)
			node.neighborhood_set[X_index] = None

			eligible_neighbors = []
			for n1 in node.neighborhood_set:
				for n2 in n1.neighborhood_set:
					if n2 not in node.neighborhood_set and n2 != node:
						eligible_neighbors.append(n2)

			eligible_neighbors = list(set(eligible_neighbors))

			closest_node = get_closest_node(eligible_neighbors, node)
			node.neighborhood_set[X_index] = closest_node

		# Repair routing table
		for row_index, row in enumerate(node.routing_table):
			if X in row:
				col_index = row.index(X)
				repair_routing_table_row(node, row_index, col_index)


def repair_routing_table_row(node, row, col):
	node.routing_table[row][col] = None
	for r in range(row, len(node.routing_table)):
		for c in range(len(node.routing_table[r])):
			temp_node = node.routing_table[r][c]
			if c != col and temp_node:
				eligible_node = temp_node[row][col]
				if eligible_node:
					node.routing_table[row][col] = eligible_node
					return

def shl(x, y):
	l = [x, y]
	return len(os.path.commonprefix(l))

def get_min_leaf_set(A):
	min_node = None
	min_index = -1
	for index, node in enumerate(A.smaller_leaf_set):
		if node:
			if not min_node:
				min_node = node
				min_index = index
			elif min_node.node_id > node.node_id:
				min_node = node
				min_index = index

	return min_node, min_index

def get_max_leaf_set(A):
	max_node = None
	max_index = -1
	for index, node in enumerate(A.larger_leaf_set):
		if node:
			if not max_node:
				max_node = node
				max_index = index
			elif max_node.node_id < node.node_id:
				max_node = node
				max_index = index

	return max_node, max_index

def get_closest_node_leaf_set(X, A):
	closest_node = None
	min_dist = math.inf

	for node in A.smaller_leaf_set + A.larger_leaf_set + [A]:
		if node:
			dist = get_key_distance(X, node)
			if dist < min_dist:
				min_dist = dist
				closest_node = node

	return closest_node

def get_key_distance(a, b):
	return abs(int(a.node_id, 16) - int(b.node_id, 16))

def get_closest_node_wrt_key(nodes, X):
	closest_node = None
	min_dist = math.inf
	for node in nodes:
		dist = get_key_distance(X, node)
		if dist < min_dist:
			min_dist = dist
			closest_node = node

	return closest_node