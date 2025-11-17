# =============================================================================
# Mumbai Logistics Advisor - FINAL CORRECTED & COMPLETE VERSION
# Name: Sia Mishra
# Roll Number: 2309659
# =============================================================================

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import math
import pandas as pd
import time

# --- CORE LOGIC: GRAPH CREATION AND ALGORITHMS ---

def create_mumbai_graph():
    G = nx.Graph()
    nodes = {
        "Bhiwandi (Warehouse)": (10, 10), "Borivali": (2, 9), "Andheri": (1, 6),
        "Powai": (4, 7), "Bandra": (3, 4), "BKC": (5, 5), "Ghatkopar": (7, 3),
        "Dadar": (5, 2), "Worli": (4, 0), "CST": (6, -2)
    }
    for node, pos_coords in nodes.items():
        G.add_node(node, pos=pos_coords)
    node_types = {node: "arterial" for node in G.nodes()}
    node_types["Bhiwandi (Warehouse)"] = "hub"
    nx.set_node_attributes(G, node_types, 'type')
    
    edges = [
        # Format: (Start, End, {distance, time_truck, time_car, time_bike, road_type})
        ("Bhiwandi (Warehouse)", "Borivali", {'distance': 30, 'time_truck': 80, 'time_car': 75, 'time_bike': 65, 'road_type': 'highway'}),
        ("Bhiwandi (Warehouse)", "Powai", {'distance': 25, 'time_truck': 65, 'time_car': 60, 'time_bike': 50, 'road_type': 'highway'}),
        ("Borivali", "Andheri", {'distance': 14, 'time_truck': 45, 'time_car': 40, 'time_bike': 30, 'road_type': 'main'}),
        ("Borivali", "Powai", {'distance': 20, 'time_truck': 55, 'time_car': 50, 'time_bike': 40, 'road_type': 'main'}),
        ("Andheri", "Bandra", {'distance': 8, 'time_truck': 30, 'time_car': 25, 'time_bike': 15, 'road_type': 'main'}),
        ("Andheri", "Powai", {'distance': 6, 'time_truck': 25, 'time_car': 20, 'time_bike': 15, 'road_type': 'narrow_lane'}),
        ("Powai", "BKC", {'distance': 10, 'time_truck': 35, 'time_car': 30, 'time_bike': 20, 'road_type': 'main'}),
        ("Powai", "Ghatkopar", {'distance': 5, 'time_truck': 20, 'time_car': 15, 'time_bike': 10, 'road_type': 'main'}),
        ("Bandra", "BKC", {'distance': 3, 'time_truck': 15, 'time_car': 10, 'time_bike': 7, 'road_type': 'main'}),
        ("Bandra", "Dadar", {'distance': 7, 'time_truck': 25, 'time_car': 20, 'time_bike': 15, 'road_type': 'main'}),
        ("BKC", "Ghatkopar", {'distance': 8, 'time_truck': 30, 'time_car': 25, 'time_bike': 20, 'road_type': 'narrow_lane'}),
        ("BKC", "Worli", {'distance': 10, 'time_truck': 40, 'time_car': 35, 'time_bike': 25, 'road_type': 'main'}),
        ("Ghatkopar", "Dadar", {'distance': 9, 'time_truck': 35, 'time_car': 30, 'time_bike': 25, 'road_type': 'main'}),
        ("Dadar", "Worli", {'distance': 5, 'time_truck': 20, 'time_car': 15, 'time_bike': 10, 'road_type': 'main'}),
        ("Worli", "CST", {'distance': 10, 'time_truck': 30, 'time_car': 25, 'time_bike': 20, 'road_type': 'main'})
    ]
    for u, v, attrs in edges:
        G.add_edge(u, v, **attrs)
    return G

COST_PARAMS = {
    "Truck": {"cost_per_km": 25, "cost_per_hour": 300},
    "Car": {"cost_per_km": 12, "cost_per_hour": 200},
    "Motorbike": {"cost_per_km": 5, "cost_per_hour": 150}
}

def calculate_trip_cost(path, G, transport_mode):
    total_distance = 0
    total_time_minutes = 0
    # --- FIX FOR MOTORBIKE ERROR IS HERE ---
    time_key = f"time_{transport_mode.lower()}"
    if transport_mode == "Motorbike":
        time_key = "time_bike" # The actual key in the data is 'time_bike'
    # --- END OF FIX ---

    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        total_distance += G[u][v]['distance']
        total_time_minutes += G[u][v][time_key]
        
    params = COST_PARAMS[transport_mode]
    cost_from_distance = total_distance * params["cost_per_km"]
    cost_from_time = (total_time_minutes / 60) * params["cost_per_hour"]
    total_cost = cost_from_distance + cost_from_time
    return total_cost

def euclidean_distance(G, node1, node2):
    pos1_x, pos1_y = G.nodes[node1]['pos']
    pos2_x, pos2_y = G.nodes[node2]['pos']
    return math.sqrt((pos2_x - pos1_x)**2 + (pos2_y - pos1_y)**2)

def get_explored_nodes(G, source, weight):
    try:
        lengths = nx.single_source_dijkstra_path_length(G, source, weight=weight)
        return list(lengths.keys())
    except nx.NetworkXNoPath:
        return []

def draw_path(G, path, title="", explored_nodes=None):
    pos = nx.get_node_attributes(G, 'pos')
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if explored_nodes:
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=explored_nodes, node_color='#e0e0e0', node_size=2000)
    
    nx.draw(G, pos, ax=ax, with_labels=True, node_color='skyblue', node_size=2000, font_size=10, font_weight='bold')
    edge_labels = {edge: f"D:{attrs['distance']}km" for edge, attrs in G.edges.items()}
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels, font_size=8, font_color='saddlebrown')
    
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=path, node_color='#90ee90', node_size=2000)
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=path_edges, edge_color='#228b22', width=3.5)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[path[0]], node_color='#ff4757', node_size=2200)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[path[-1]], node_color='#ffa502', node_size=2200)

    ax.set_title(title, size=16, weight='bold')
    fig.tight_layout()
    return fig

# --- STREAMLIT WEB APP INTERFACE ---

st.set_page_config(page_title="Mumbai Logistics Advisor", page_icon="🚚", layout="wide")
if 'city_map' not in st.session_state:
    st.session_state.city_map = create_mumbai_graph()

st.title("🗺️ Mumbai Logistics Advisor")

with st.sidebar:
    st.title("📍 Route Controls")
    node_list = list(st.session_state.city_map.nodes())
    start_node = st.selectbox("Start Location:", node_list, index=node_list.index("Bhiwandi (Warehouse)"))
    end_node = st.selectbox("End Location:", node_list, index=node_list.index("CST"))
    transport_mode = st.selectbox("Mode of Transport:", ("Truck", "Car", "Motorbike"))
    optimization_criteria = st.radio("Optimize for:", ('time', 'distance'), format_func=lambda x: "⚡ Fastest (Time)" if x == 'time' else "💰 Cheapest (Distance)")

    st.divider()
    st.title("🚦 Simulation Controls")
    is_rush_hour = st.checkbox("Simulate Evening Rush Hour")
    road_closure_options = ["None"] + [f"{u} - {v}" for u, v in st.session_state.city_map.edges()]
    closed_road = st.selectbox("Simulate Road Closure:", road_closure_options)

if st.button("Find Optimal Route", type="primary", use_container_width=True):
    with st.spinner("🧠 Calculating the best route..."):
        time.sleep(1)
        
        current_map = st.session_state.city_map.copy()
        
        if transport_mode == "Truck":
            restricted_edges = [(u, v) for u, v, data in current_map.edges(data=True) if data.get('road_type') == 'narrow_lane']
            current_map.remove_edges_from(restricted_edges)

        # --- FIX FOR MOTORBIKE ERROR IS HERE ---
        time_key_for_vehicle = f"time_{transport_mode.lower()}"
        if transport_mode == "Motorbike":
            time_key_for_vehicle = "time_bike" # Correct key
        # --- END OF FIX ---
        
        if is_rush_hour:
            rush_hour_multipliers = {"Truck": 2.0, "Car": 1.75, "Motorbike": 1.25}
            multiplier = rush_hour_multipliers[transport_mode]
            for u, v, data in current_map.edges(data=True):
                if time_key_for_vehicle in data:
                    data[time_key_for_vehicle] = int(data[time_key_for_vehicle] * multiplier)
        
        if closed_road != "None":
            u, v = closed_road.split(" - ")
            if current_map.has_edge(u, v):
                current_map.remove_edge(u, v)

        weight_key = time_key_for_vehicle if optimization_criteria == 'time' else 'distance'

        try:
            a_star_path = nx.astar_path(current_map, start_node, end_node, heuristic=lambda u,v: euclidean_distance(current_map, u, v), weight=weight_key)
            inr_cost = calculate_trip_cost(a_star_path, current_map, transport_mode)
            
            st.header("📊 Results")
            with st.container(border=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    metric_label = "Fastest Time" if optimization_criteria == 'time' else "Shortest Distance"
                    metric_value = f"{nx.path_weight(current_map, a_star_path, weight=weight_key)} {'mins' if optimization_criteria == 'time' else 'km'}"
                    st.metric(label=metric_label, value=metric_value)
                with col2:
                    st.metric(label="Estimated Trip Cost", value=f"₹ {inr_cost:.2f}")
                with col3:
                    st.metric(label="Vehicle", value=transport_mode)
                
                st.divider()
                col_itinerary, col_map = st.columns([1, 1.5])
                with col_itinerary:
                    st.success(f"Optimal path for a **{transport_mode}**!")
                    st.write("**Route:**")
                    st.write(" → ".join(a_star_path))
                    with st.expander("📜 Show Detailed Itinerary"):
                        itinerary_html = "<ul>"
                        for i in range(len(a_star_path) - 1):
                            leg_start, leg_end = a_star_path[i], a_star_path[i+1]
                            leg_cost = current_map[leg_start][leg_end][weight_key]
                            cost_unit = "mins" if optimization_criteria == 'time' else "km"
                            itinerary_html += f"<li><b>{leg_start}</b> to <b>{leg_end}</b> (Cost: {leg_cost} {cost_unit})</li>"
                        itinerary_html += "</ul>"
                        st.markdown(itinerary_html, unsafe_allow_html=True)
                with col_map:
                    fig = draw_path(current_map, a_star_path, f"Optimal Route for a {transport_mode}")
                    st.pyplot(fig)

            # --- ALGORITHMIC ANALYSIS SECTION (RESTORED) ---
            st.header("⚙️ Algorithmic Efficiency Analysis")
            with st.container(border=True):
                st.markdown("This section visually demonstrates *why* A* is more efficient than a blind search algorithm like Dijkstra.")
                comp_col1, comp_col2 = st.columns(2)
                with comp_col1:
                    st.subheader("A* Search Exploration")
                    astar_explored = set(a_star_path)
                    for node in a_star_path:
                        astar_explored.update(current_map.neighbors(node))
                    fig_a_star = draw_path(current_map, a_star_path, "A* Search (Path Found)", explored_nodes=list(astar_explored))
                    st.pyplot(fig_a_star)
                    st.info(f"A* is 'informed'. It focuses its search (grey nodes) towards the goal.")
                with comp_col2:
                    st.subheader("Dijkstra's Search Exploration")
                    dijkstra_explored = get_explored_nodes(current_map, start_node, weight=weight_key)
                    fig_dijkstra = draw_path(current_map, a_star_path, "Dijkstra's Search (Path Found)", explored_nodes=dijkstra_explored)
                    st.pyplot(fig_dijkstra)
                    st.warning(f"Dijkstra is 'blind'. It explores in all directions (grey nodes) until it finds the target.")

        except nx.NetworkXNoPath:
            st.error(f"No path could be found for a **{transport_mode}** between {start_node} and {end_node}.")
            st.warning("This may be due to road closures or vehicle restrictions.")
            fig = draw_path(current_map, path=None, title=f"Map View: No Path Found")
            st.pyplot(fig)
else:
    st.info("Select your route controls in the sidebar and click 'Find Optimal Route' to begin.")
    fig = draw_path(st.session_state.city_map, path=None, title="Mumbai City Map Overview")
    st.pyplot(fig)