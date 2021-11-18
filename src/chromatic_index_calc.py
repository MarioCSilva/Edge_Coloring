import logging

import networkx as nx
import time
from matplotlib import colors as mcolors
import numpy as np


class Chromatic_Index_Calc:
    """
	This class finds the chromatic index of a given Graph object.
	"""
    def __init__(self):
        self.seed = 93430
        self.colors = list(mcolors.CSS4_COLORS.values())
        np.random.seed(self.seed)
        np.random.shuffle(self.colors)


    def greedy_coloring(self, G, order_degree_heur):
        start_time = time.time()

        edges_colors = {edge: -1 for edge in G.edges()}
        edges = list(G.edges())
        current_new_color = 0

        # get adjacency matrix for edges and list of ordered edges descending by their edge connectivity
        adjacent_edges = self.edge_connectivity(edges)

        # sort by highest edge connectivity
        if order_degree_heur:
            ordered_edges = sorted(edges, key= lambda x: len(adjacent_edges[x]), reverse=True)
        else:
            ordered_edges = edges
        
        # 1st heuristic
        # assign colors to the first highest adjacent edge first
        highest_conn_edge = ordered_edges.pop(0)
        edges_colors, current_new_color = \
            self.assign_color(edges_colors, highest_conn_edge, current_new_color, current_new_color)

        # second heuristic + greedy approach
        # color edges starting by the highest adjacent edges
        for edge in ordered_edges:

            # skip if edge has a color already assigned
            if edges_colors[edge] != -1:
                continue

            # temporary sets to store used colors by adjacent edges
            # and the adjacent edges that are uncolored so they can be assigned later
            used_colors = set()
            for e in adjacent_edges[edge]:
                if edges_colors[e] != -1:
                    used_colors.add(edges_colors[e])

            # get available color for this edge
            available_color = self.get_available_color(current_new_color, used_colors)

            # assign available color to current edge
            edges_colors, current_new_color = \
                self.assign_color(edges_colors, edge, current_new_color, available_color)

        chromatic_Index = current_new_color

        total_time = time.time() - start_time

        nx.set_edge_attributes(G,
            {edge: self.colors[color] for edge, color in edges_colors.items()},
            'color')

        return chromatic_Index, G, total_time


    def get_available_color(self, current_new_color, used_colors):
        color = min([y for y in range(current_new_color) if y not in used_colors],\
                    default=current_new_color)
        return color


    def assign_color(self, edges_colors, edge, current_new_color, color):
        # assign available color to edge
        edges_colors[edge] = color
        
        # if available color is equal to new color,
        # means that the new color has to be used
        if current_new_color == color:
            current_new_color += 1
        
        return edges_colors, current_new_color


    def edge_connectivity(self, edges):
        num_edges = len(edges)
        adjacent_edges = {edge: set() for edge in edges}
        # only go through like the top side of a matrix above diagonal
        for i in range(num_edges - 1):
            e1_n1, e1_n2 = edges[i]
            for i2 in range(i, num_edges):
                if edges[i] == edges[i2]:
                    continue
                if e1_n1 in edges[i2] or e1_n2 in edges[i2]:
                    adjacent_edges[edges[i]].add(edges[i2])
                    adjacent_edges[edges[i2]].add(edges[i])
        return adjacent_edges


    def exhaustive_coloring(self, G, vizing_theorem):
        start_time = time.time()

        edges = list(G.edges())

        # Create a dictionary that stores the colors
        # initializing all edges with color 0    
        edges_colors = {edge: -1 for edge in G.edges()}

        # get edges adjacency dict
        edge_adj = self.edge_connectivity(edges)

        # Vizing Theorem
        if vizing_theorem:
            highest_node_degree = sorted(G.degree, key=lambda x: x[1], reverse=True)[0][1]
            m_values = [highest_node_degree, highest_node_degree + 1]
        else:
            m_values = [1]

        while True:
            m = m_values.pop()
            # start search on the first edge of index 0
            edges_colors = self.m_color_search_backtrack(edge_adj, m, edges, edges_colors, 0)
            if edges_colors:
                chromatic_Index = m
                break
            edges_colors = {edge: -1 for edge in G.edges()}
            if not vizing_theorem:
                m_values.append(m*1)

        total_time = time.time() - start_time

        nx.set_edge_attributes(G,
            {edge: self.colors[color] for edge, color in edges_colors.items()},
            'color')
        
        return chromatic_Index, G, total_time


    def m_color_search_backtrack(self, edge_adj, m, edges, edges_colors, edge_ind):
        # all edges colored then return
        if edge_ind == len(edges):
            return edges_colors

        edge = edges[edge_ind]

        # try different colors for edge
        for c in range(m):
            # check if edge can be colored with this color
            flag = True
            for adj_edge in edge_adj[edge]:
                if c == edges_colors[adj_edge]:
                    flag = False
                    break
            if flag:
                # assign color if no conflictions
                edges_colors[edge] = c
                # recursion to check other vertices
                result = self.m_color_search_backtrack(edge_adj, m, edges, edges_colors, edge_ind+1)
                if result:
                    return result
                # if color gives no solution, reset color and backtracks here
                edges_colors[edge] = -1
        return None