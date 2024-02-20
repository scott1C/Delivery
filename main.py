import os
import random
import math
import osmnx as ox

def generate_permutations(arr):
    result = []
    n = len(arr)
    
    def backtrack(start):
        if start == n:
            result.append(arr.copy())
            return
        for i in range(start, n):
            arr[start], arr[i] = arr[i], arr[start]
            backtrack(start + 1)
            arr[start], arr[i] = arr[i], arr[start]

    backtrack(0)
    return result

file_path = os.path.join(os.path.dirname(__file__), "map.osm")
G = ox.graph_from_xml(file_path)

# Gets all the nodes and edges from the graph G
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

# Extract nodes from the graph
nodes = list(G.nodes)

# Randomly select four nodes
random_nodes = random.sample(nodes, 4)

permutations = generate_permutations(random_nodes)

shortest_path_legth = math.inf
for permutation in permutations:
    path_length = 0
    for i in range(len(permutation) - 1):
        # Getting the route from node X to node Y
        route = ox.shortest_path(G, permutation[i], permutation[i + 1], weight='length')
        # Convert the route to a GeoDataFrame
        route_gdf = ox.utils_graph.route_to_gdf(G, route, 'length')
        # Calculate the total length of the route
        path_length += route_gdf['length'].sum()
    if path_length < shortest_path_legth:
        shortest_path_legth = path_length

print(f"{shortest_path_legth:.3f}")

#TODO: 
# To find a method how to display here the graph with the shortest path which will traverse every node given 