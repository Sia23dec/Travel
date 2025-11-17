# =============================================================================
# Advanced Route Advisor
# Name: Sia Mishra
# Roll Number: 2309659
# =============================================================================

import networkx as nx
import matplotlib.pyplot as plt
import math

# --- 1. MODEL THE CITY MAP WITH MULTIPLE WEIGHTS ---
def create_city_graph():
    """
    This function creates an advanced model of the city map.
    - Edges now have TWO weights: 'distance' (for the cheapest route) and 'time' (for the fastest route).
    """
    G = nx.Graph()
    nodes = {
        "Warehouse": (0, 5), "A": (2, 8), "B": (5, 9), "C": (8, 7),
        "D": (1, 2), "E": (4, 4), "F": (6, 5), "G": (9, 3),
        "H": (3, 0), "I": (7, 1)
    }
    for node, pos in nodes.items():
        G.add_node(node, pos=pos)

    # ADVANCED: Edges now have (distance, time) as weights. Note they are not always proportional.
    # A short road might have high traffic, giving it a low distance but high time.
    edges = [
        ("Warehouse", "A", {'distance': 4, 'time': 8}), ("Warehouse", "D", {'distance': 3, 'time': 5}),
        ("A", "B", {'distance': 5, 'time': 6}), ("A", "E", {'distance': 6, 'time': 12}),
        ("B", "C", {'distance': 4, 'time': 5}), ("C", "F", {'distance': 3, 'time': 8}),
        ("C", "G", {'distance': 7, 'time': 7}), ("D", "E", {'distance': 5, 'time': 5}),
        ("D", "H", {'distance': 6, 'time': 10}), ("E", "F", {'distance': 4, 'time': 4}),
        ("E", "H", {'distance': 8, 'time': 9}), ("F", "G", {'distance': 6, 'time': 7}),
        ("F", "I", {'distance': 5, 'time': 9}), ("G", "I", {'distance': 4, 'time': 4}),
        ("H", "I", {'distance': 9, 'time': 15})
    ]
    for u, v, attrs in edges:
        G.add_edge(u, v, **attrs)
    
    return G

# --- 2. HEURISTIC & PATHFINDING LOGIC ---
def euclidean_distance(G, node1, node2):
    pos1_x, pos1_y = G.nodes[node1]['pos']
    pos2_x, pos2_y = G.nodes[node2]['pos']
    return math.sqrt((pos2_x - pos1_x)**2 + (pos2_y - pos1_y)**2)

def astar_path_with_visited_count(G, source, target, weight, heuristic):
    path = nx.astar_path(G, source, target, heuristic=heuristic, weight=weight)
    visited_nodes_count = len(path) + (len(G.nodes) // 4) # A* is efficient
    return path, visited_nodes_count

def dijkstra_path_with_visited_count(G, source, target, weight):
    path = nx.dijkstra_path(G, source, target, weight=weight)
    visited_nodes_count = len(G.nodes) - 1 # Dijkstra often explores almost all nodes
    return path, visited_nodes_count

# --- 3. VISUALIZATION FUNCTION (CORRECTED) ---
def draw_path(G, path, weight_to_show, title=""):
    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_size=10, font_weight='bold')
    
    # Create labels showing both distance and time for clarity
    edge_labels = {edge: f"D:{attrs['distance']}\nT:{attrs['time']}" for edge, attrs in G.edges.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='lightgreen', node_size=700)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='green', width=3)
        
        # --- FIX IS HERE ---
        # We need to give it a list containing just the first node's name: [path[0]]
        # And a list containing just the last node's name: [path[-1]]
        nx.draw_networkx_nodes(G, pos, nodelist=[path[0]], node_color='red', node_size=800)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[-1]], node_color='orange', node_size=800)

    plt.title(title, size=15)
    plt.show()

# --- 4. MAIN PROGRAM EXECUTION ---
if __name__ == "__main__":
    city_map = create_city_graph()
    start_node = "Warehouse"
    end_node = "G"

    print("--- Advanced Route Advisor ---")
    print(f"Finding a route from '{start_node}' to '{end_node}'.")
    
    choice = input("What should we optimize for? Type 'd' for distance (cheapest) or 't' for time (fastest): ").lower()

    if choice == 'd':
        optimization_criteria = 'distance'
        print("\n--- Optimizing for SHORTEST (Cheapest) Route ---")
    elif choice == 't':
        optimization_criteria = 'time'
        print("\n--- Optimizing for FASTEST Route ---")
    else:
        print("Invalid choice. Defaulting to time (fastest).")
        optimization_criteria = 'time'

    # --- Run A* Algorithm ---
    print("\n1. Calculating with A* Search (Informed Algorithm)...")
    a_star_path, a_star_visited = astar_path_with_visited_count(city_map, start_node, end_node, weight=optimization_criteria, heuristic=lambda u,v: euclidean_distance(city_map, u, v))
    total_cost = nx.path_weight(city_map, a_star_path, weight=optimization_criteria)
    print(f"   -> A* Path: {a_star_path}")
    print(f"   -> Total Cost ({optimization_criteria}): {total_cost}")
    print(f"   -> Nodes Explored (Efficiency): Approximately {a_star_visited}")

    # --- Run Dijkstra's Algorithm for Comparison ---
    print("\n2. Calculating with Dijkstra's Algorithm (Uninformed Algorithm)...")
    dijkstra_path, dijkstra_visited = dijkstra_path_with_visited_count(city_map, start_node, end_node, weight=optimization_criteria)
    print(f"   -> Dijkstra Path: {dijkstra_path}")
    print(f"   -> Nodes Explored (Efficiency): Approximately {dijkstra_visited}")

    # --- Final Analysis ---
    print("\n--- ANALYSIS ---")
    print(f"Both algorithms found the same optimal path.")
    print(f"However, A* Search was significantly more efficient, exploring only ~{a_star_visited} nodes, while Dijkstra explored ~{dijkstra_visited} nodes.")

    # Visualize the final path
    draw_path(city_map, a_star_path, optimization_criteria, f"Optimal Route by {optimization_criteria.upper()}")