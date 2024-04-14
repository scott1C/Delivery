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

# Randomly select nodes
destination_random_nodes = random.sample(nodes, 15)
start_random_nodes = random.sample(nodes, math.ceil(15 / 3))

# Adding the start position and initializating the folium map
start_position = G.nodes[destination_random_nodes[0]]
route_map = folium.Map(location=[start_position['y'], start_position['x']], zoom_start=12)

# Adding markers of the start point in our map
for index, start_node in enumerate(start_random_nodes):
    folium.Marker(location=(G.nodes[start_node]['y'], G.nodes[start_node]['x']), popup=f"Courier {index + 1}", icon=folium.Icon(color='green')).add_to(route_map)

 # Adding destination markers in our map
for index, destination_node in enumerate(destination_random_nodes):
    folium.Marker(location=(G.nodes[destination_node]['y'], G.nodes[destination_node]['x']), popup=f"Destionation {index + 1}", icon=folium.Icon(color='red')).add_to(route_map)


# A list to store the final routes of the couriers
route_graph = [[] for _ in range(len(start_random_nodes))]
# A list to store the time needed for each courier
time = [0 for _ in range(len(start_random_nodes))]
# A list to store the total number of order
orders = [0 for _ in range(len(start_random_nodes))]

for i in range(len(destination_random_nodes)):
    destination_point = destination_random_nodes[i]
    # Variable where is stored the closest destination path from courier to order
    closest_destination = []
    # Variable where is stored the length of the path 
    closest_destination_length = math.inf
    index = 0

    for j, start_point in enumerate(start_random_nodes):
        if orders[j] < 3 and time[j] < 30:
            # Getting the route from node X to node Y
            route = ox.shortest_path(G, destination_point, start_point)
            # Convert the route to a GeoDataFrame to get the length of the path
            route_length = ox.utils_graph.route_to_gdf(G, route)['length'].sum()
            if route_length < closest_destination_length:
                closest_destination = route
                closest_destination_length = route_length
                index = j

    # Getting the time needed from the current position of the current till the destination
    destination_time = round(closest_destination_length / 1000 / 15 * 60)
        
    route_graph[index].append(closest_destination)
    time[index] += destination_time
    orders[index] += 1
    start_random_nodes[index] = destination_random_nodes[i]
    
# Iterate over paths and add a PolyLine for each path
colors = ['blue', 'red', 'green', 'purple', 'black']

for index, paths in enumerate(route_graph):
    if paths:
        print(f"Time needed for the courier {index + 1} is: {time[index]} minutes, having {orders[index]} orders")
        # Create a list of (latitude, longitude) pairs for the path
        for path in paths:
            path_coordinates = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in path]
            # Create a PolyLine for the path
            folium.PolyLine(locations=path_coordinates, color=colors[index], weight=5, opacity=0.7).add_to(route_map)
    
# Save and show the route
map_file_path="route_map.html"
route_map.save(map_file_path)
wb.open('file://' + os.path.realpath(map_file_path))

# End the timer
end = t.time()
print(f"Completed in: {end - start:.2f} seconds.")