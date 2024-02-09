import os
import osmnx as ox
import networkx as nx

file_path = os.path.join(os.path.dirname(__file__), "map.osm")
G = ox.graph_from_xml(file_path)

# Gets all the nodes and edges from the graph G
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

# To plot the created graph
ox.plot_graph(G)
