import sys
import argparse
import logging
from graph_manager import Graph_Manager
from chromatic_index import Chromatic_Index

class Main:
	def __init__(self):
		self.check_arguments()


	def usage(self):
		print("Usage: python3 main.py\
			\n\t-i <Directory name for indexation:str>\
			\n\t-f <File Name for data set:str>\
			\n\t-m <Minimum Length Filter>\
			\n\t-l <Length for Minimum Length Filter:int>\
			\n\t-p <Porter Stemmer Filter>\
			\n\t-stopwords <Stop Words Filter>\
			\n\t -stopwords_file <Stop Words File>\
			\n\t-mp <Map Reduce>\
			\n\t-search <Search Engine>")
		sys.exit()


	def check_arguments(self):
		arg_parser = argparse.ArgumentParser(
			prog="Indexer",
			usage=self.usage
		)
		arg_parser.add_argument('-help', action='store_true')
		arg_parser.add_argument('-index_dir', nargs=1, default=[''])
		arg_parser.add_argument('-file_name', nargs=1, default=['amazon_reviews.tsv'])
		arg_parser.add_argument('-min_length', action='store_true')
		arg_parser.add_argument('-length', nargs=1, type=int)
		arg_parser.add_argument('-porter', action='store_true')
		arg_parser.add_argument('-stopwords', action='store_true')
		arg_parser.add_argument('-stopwords_file', nargs=1,  default=['stopwords.txt'])
		arg_parser.add_argument('-search', action='store_true')
		arg_parser.add_argument('-mp', action='store_true')
		arg_parser.add_argument('-positions', action='store_true')

		try:
			args = arg_parser.parse_args()
		except:
			self.usage()

		if args.help:
			self.usage()

		self.search = args.search
		self.index_dir = args.index_dir[0]
		file_name = args.file_name[0]
		if self.index_dir == "":
			self.index_dir = file_name.split('.')[0]
		min_len = args.length[0] if args.min_length and args.length else None

		return self.index_dir, file_name, args.min_length, min_len, args.porter,\
			args.stopwords, args.stopwords_file[0], args.mp, args.positions


if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

	main = Main()