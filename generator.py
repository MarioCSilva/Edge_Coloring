import logging
from graph import Graph
from random import randrange
import networkx as nx
import matplotlib.pyplot as plt


class Graph_Generator:
	"""
	This class creates graphs that obey the following rules:
		- vertices are 2D points on the XOY plane, with integer valued
		coordinates between 1 and 9.
		- vertices should neither be coincident nor too close.
		- the number of edges sharing a vertex is randomly determined.
	"""
	def __init__(self):
		self.num_vertices = randrange(10)
		self.num_edges = self.num_vertices - 1

		logging.info(f"Generated Graph with {self.num_vertices} vertices and {self.num_edges}")

		g = nx.generators.lattice.grid_2d_graph(10, 10)

		nodes_to_remove = [(0, i) for i in range(10)]
		nodes_to_remove.extend([(i, 0) for i in range(1,10)])

		g.remove_nodes_from(nodes_to_remove)

		nx.draw(g, with_labels=True, font_weight='bold')
		print(list(g.neighbors((2,4))))
		plt.show()


	def generate(self):
		pass

Graph_Generator()