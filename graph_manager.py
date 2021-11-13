import logging
from random import randint, random, choice, seed
import networkx as nx
import matplotlib.pyplot as plt
import os
from itertools import combinations, groupby, product
from networkx.drawing.nx_pydot import write_dot


class Graph_Manager:
	"""
	This class creates graphs that obey the following rules:
		- vertices are 2D points on the XOY plane, with integer valued
		coordinates between 1 and 9.
		- vertices should neither be coincident nor too close.
		- the number of edges sharing a vertex is randomly determined.
	"""
	def __init__(self):
		self.GRAPH_DIRECTORY = './graphs/'
		self.SEED = 93430


	def generate(self, num_nodes):
		"""
		Generates a random undirected graph, similarly to an Erdős-Rényi 
		graph, but enforcing that the resulting graph is conneted
		"""
		assert num_nodes > 1 and num_nodes < 82, "Can only have between 2 to 81 nodes with 2D dimensional coordinates from 1 to 9"

		seed(self.SEED)

		edge_prob = random()
		all_possible_edges = combinations(range(num_nodes), 2)

		G = nx.Graph()
		G.add_nodes_from(range(num_nodes))

		if edge_prob <= 0:
			return G
		if edge_prob >= 1:
			return nx.complete_graph(nodes, create_using=G)
		for _, node_edges in groupby(all_possible_edges, key=lambda x: x[0]):
			node_edges = list(node_edges)
			random_edge = choice(node_edges)
			G.add_edge(*random_edge)
			for e in node_edges:
				if random() < edge_prob:
					G.add_edge(*e)

		node_positions = nx.spring_layout(G, k=2, scale=4, center=(5,5), seed=self.SEED)
		positions = { node: (int(pos[0]), int(pos[1])) for node, pos in node_positions.items() }

		all_possible_coords = [x for x in product((1,2,3,4,5,6,7,8,9), repeat=2) if x not in positions.values()]
		for n1 in sorted(positions.keys()):
			for n2 in sorted(positions.keys()):
				if n1 != n2 and positions[n1] == positions[n2]:
					rand_index = randint(0, len(all_possible_coords)-1)
					new_pos = all_possible_coords[rand_index]
					del all_possible_coords[rand_index]
					positions[n2] = new_pos


		nx.set_node_attributes(G, positions, 'pos')
		nodes_to_str = {n:str(n) for n in G.nodes()}
		G = nx.relabel_nodes(G, nodes_to_str, copy=True)

		logging.info(f"Generated Connected Graph with {num_nodes} vertices and {len(G.edges())}, probability of edges {edge_prob}\n")
		logging.info(f"Graph Nodes:\n{G.nodes(data=True)}\n")
		logging.info(f"Graph Edges:\n{G.edges()}\n")

		self.save_graph(G, num_nodes)
	
		return G


	def show_graph(self, G):
		positions = {n:data['pos'] for n, data in G.nodes(data=True)}

		fig, ax = plt.subplots()

		nx.draw(G, positions, with_labels=True, font_weight='bold', ax=ax, node_size=700, font_size=7.5)

		limits=plt.axis('on')
		plt.xticks([1,2,3,4,5,6,7,8,9])
		plt.yticks([1,2,3,4,5,6,7,8,9])
		ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
		plt.grid()
		plt.show()
		plt.clf()
		plt.cla()
		plt.close()


	def save_graph(self, G, num_nodes):
		positions = {n:data['pos'] for n, data in G.nodes(data=True)}

		fig, ax = plt.subplots()
		nx.draw(G, positions, with_labels=True, font_weight='bold', ax=ax, node_size=700, font_size=7.5)
		limits=plt.axis('on')
		plt.xticks([1,2,3,4,5,6,7,8,9])
		plt.yticks([1,2,3,4,5,6,7,8,9])
		ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
		plt.grid()

		logging.info(f"Saving graph to file: Graph_{num_nodes}.txt and Graph_{num_nodes}.png")
		plt.savefig(f"{self.GRAPH_DIRECTORY}Graph_{num_nodes}.png", bbox_inches='tight')
		plt.clf()
		plt.cla()
		plt.close()
		nx.write_gml(G, f"{self.GRAPH_DIRECTORY}Graph_{num_nodes}.txt")


	def load_graph(self, num_nodes):
		try:
			logging.info(f"Retrieving graph from saved files")
			G = nx.read_gml(f"{self.GRAPH_DIRECTORY}Graph_{num_nodes}.txt")
			positions = {n:data['pos'] for n, data in G.nodes(data=True)}
		except FileNotFoundError:
			logging.info(f"Didn't found a graph saved with this number of nodes, generating one instead")
			G = self.generate(num_nodes)
			positions = {n:data['pos'] for n, data in G.nodes(data=True)}

		return G, positions
