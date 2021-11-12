import logging
from graph import Graph
from random import randint, random, choice, seed
import networkx as nx
import matplotlib.pyplot as plt
import os
from itertools import combinations, groupby


class Graph_Manager:
	"""
	This class creates graphs that obey the following rules:
		- vertices are 2D points on the XOY plane, with integer valued
		coordinates between 1 and 9.
		- vertices should neither be coincident nor too close.
		- the number of edges sharing a vertex is randomly determined.
	"""
	def __init__(self, num_nodes=randint(2, 20)):
		self.num_nodes = num_nodes
		self.GRAPH_DIRECTORY = './graphs/'
		self.SEED = 93430

		seed(self.SEED)


	def generate(self):
		"""
		Generates a random undirected graph, similarly to an Erdős-Rényi 
		graph, but enforcing that the resulting graph is conneted
		"""
		edge_prob = random()
		all_possible_edges = combinations(range(self.num_nodes), 2)

		G = nx.Graph()
		G.add_nodes_from(range(self.num_nodes))

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

		node_positions = nx.spring_layout(G, k=0.15, scale=4, seed=self.SEED)
		positions = { node: (int(pos[0]+5),int(pos[1]+5)) for node, pos in node_positions.items() }
		G = nx.relabel_nodes(G, positions, copy=True)
		positions = { x: x for x in positions.values()}

		logging.info(f"Generated Connected Graph with {self.num_nodes} vertices and {len(G.edges())}, probability of edges {edge_prob}\n")
		logging.info(f"Graph Nodes:\n{G.nodes()}\n")
		logging.info(f"Graph Edges:\n{G.edges()}\n")

		self.save_graph(G, positions)
	
		return G



	def save_graph(self, G, positions):
		fig, ax = plt.subplots()
		nx.draw(G, positions, with_labels=True, font_weight='bold', ax=ax, node_size=700, font_size=7.5)
		limits=plt.axis('on')
		ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
		plt.grid()

		plt.savefig(f"{self.GRAPH_DIRECTORY}Graph_{self.num_nodes}.png", bbox_inches='tight')

		plt.show()




gm = Graph_Manager()
gm.generate()