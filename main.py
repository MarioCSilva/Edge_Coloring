import sys
import argparse
import logging
from graph_manager import Graph_Manager
from chromatic_index import Chromatic_Index

class Main:
	def __init__(self):
		self.num_nodes, self.generate, self.show_graph = self.check_arguments()
		self.graph_manager = Graph_Manager()

		self.handle_args()


	def usage(self):
		print("Usage: python3 main.py\
			\n\t-n <Number of Nodes for the Graph to be used for any operation: int>\
			\n\t-g <Generate Graph>")
		sys.exit()


	def check_arguments(self):
		arg_parser = argparse.ArgumentParser(
			prog="Indexer",
			usage=self.usage
		)
		arg_parser.add_argument('-help', action='store_true')
		arg_parser.add_argument('-num_nodes', nargs=1, type=int, default=[4])
		arg_parser.add_argument('-generate', action='store_true')
		arg_parser.add_argument('-show_graph', action='store_true')


		try:
			args = arg_parser.parse_args()
		except:
			self.usage()

		if args.help:
			self.usage()

		return args.num_nodes[0], args.generate, args.show_graph


	def handle_args(self):
		if self.generate:
			print(self.num_nodes, type(self.num_nodes))
			G = self.graph_manager.generate(self.num_nodes)
			if self.show_graph:
				self.graph_manager.show_graph(G)
			return


if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

	main = Main()