import sys
import argparse
import logging
from graph_manager import Graph_Manager
from chromatic_index_calc import Chromatic_Index_Calc


class Main:
	def __init__(self):
		self.num_nodes, self.generate, self.show_graph,\
			self.exhaustive, self.greedy, self.order_degree_heur, self.vizing_theorem =\
			self.check_arguments()
		
		self.graph_manager = Graph_Manager()
		self.ci_calculator = Chromatic_Index_Calc()

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
		arg_parser.add_argument('-greedy', action='store_true')
		arg_parser.add_argument('-exhaustive', action='store_true')
		arg_parser.add_argument('-vizing_theorem', action='store_true')
		arg_parser.add_argument('-show_graph', action='store_true')
		arg_parser.add_argument('-order_degree_heur', action='store_true')

		try:
			args = arg_parser.parse_args()
		except:
			self.usage()

		if args.help:
			self.usage()

		return args.num_nodes[0], args.generate, args.show_graph,\
			args.exhaustive, args.greedy, args.order_degree_heur, args.vizing_theorem


	def handle_args(self):
		G = None
		if self.generate:
			G = self.graph_manager.generate(self.num_nodes)
			if self.show_graph:
				self.graph_manager.show_graph(G)
		if not G:
			G = self.graph_manager.load_graph(self.num_nodes)

		if self.exhaustive:
			self.handle_results(*self.ci_calculator.exhaustive_coloring(G, self.vizing_theorem),\
				"Exhaustive" + ('_Vizing' if self.vizing_theorem else ''))

		if self.greedy:
			self.handle_results(*self.ci_calculator.greedy_coloring(G, self.order_degree_heur),\
				"Greedy_Heuristics")


	def handle_results(self, ci, colored_G, total_time, strategy):
		logging.info(f"Chromatic Index Calculated with {strategy} search: {ci}")
		logging.info(f"Time to Find: {total_time} seconds")

		# store graph png and txt later on a different dir (colored graphs)

		if self.show_graph:
			self.graph_manager.show_graph(colored_G)
		
		self.graph_manager.save_graph(colored_G, strategy)


if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

	main = Main()