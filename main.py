import os
import random
import math
import osmnx as ox
import time as t
import folium
import webbrowser as wb

# Start the timer
start = t.time()

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

    # Set the backtrack to 1 so that it excludes the 1st element
    backtrack(1)
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

shortest_path_length = math.inf

# A list to store the final route
route_graph = []
for permutation in permutations:
    path_length = 0
    # A list to store the intermediate route
    list_of_routes = []
    for i in range(len(permutation) - 1):
        # Getting the route from node X to node Y
        route = ox.shortest_path(G, permutation[i], permutation[i + 1], weight='length')
        list_of_routes.append(route)
        # Convert the route to a GeoDataFrame
        route_gdf = ox.utils_graph.route_to_gdf(G, route, 'length')
        # Calculate the total length of the route
        path_length += route_gdf['length'].sum()

    if path_length < shortest_path_length:
        shortest_path_length = path_length
        # Save the route
        route_graph = list_of_routes.copy()

start_node = G.nodes[route_graph[0][0]]
route_map = folium.Map(location=[start_node['y'], start_node['x']], zoom_start=12)

# Adding marker of the start point in our path
start_marker = folium.Marker(location=(G.nodes[route_graph[0][0]]['y'], G.nodes[route_graph[0][0]]['x']), popup='Start', icon=folium.Icon(color='green')).add_to(route_map)

# Iterate over paths and add a PolyLine for each path
destination_number = 1
for path in route_graph:
    # Create a list of (latitude, longitude) pairs for the path
    path_coordinates = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in path]

    # Create a PolyLine for the path
    folium.PolyLine(locations=path_coordinates, color='blue', weight=5, opacity=0.7).add_to(route_map)

    # Adding destination markers on our path
    folium.Marker(location=(G.nodes[path[-1]]['y'], G.nodes[path[-1]]['x']), popup=f"{destination_number}", icon=folium.Icon(color='red')).add_to(route_map)
    destination_number += 1


# Save and show the route
map_file_path="route_map.html"
route_map.save(map_file_path)
wb.open('file://' + os.path.realpath(map_file_path))

# End the timer
end = t.time()
print(f"Completed in: {end - start:.2f} seconds.")