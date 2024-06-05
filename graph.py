import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Function to calculate the algebraic connectivity
def algebraic_connectivity(G):
    if len(G.nodes) < 2:
        return 0
    L = nx.laplacian_matrix(G).todense()
    eigenvalues = np.linalg.eigvalsh(L)
    return sorted(eigenvalues)[1] if len(eigenvalues) > 1 else 0  # second smallest eigenvalue or 0 if not enough eigenvalues

# Function to generate a random graph
def generate_graph():
    try:
        n_nodes = int(entry_nodes.get())
        n_edges = int(entry_edges.get())
        G.clear()
        G.add_nodes_from(range(n_nodes))
        while len(G.edges) < n_edges:
            u, v = np.random.choice(n_nodes, 2, replace=False)
            G.add_edge(u, v)
        update_plot()
        log_text.insert(tk.END, f"Generated graph with {n_nodes} nodes and {n_edges} edges.\n")
    except ValueError:
        log_text.insert(tk.END, "Please enter valid integers for nodes and edges.\n")

# Function to constrain the graph to its minimal connected structure
def constrain_to_minimal_connected_structure():
    if len(G.nodes) < 2:
        log_text.insert(tk.END, "Graph must have at least 2 nodes to create a minimal connected structure.\n")
        return
    
    # Compute the minimum spanning tree
    mst = nx.minimum_spanning_tree(G)
    G.clear()
    G.add_edges_from(mst.edges)
    update_plot()
    log_text.insert(tk.END, "Constrained graph to its minimal connected structure.\n")

# Function to truncate the graph to its largest connected component
def truncate_to_largest_component():
    if len(G.nodes) < 2:
        log_text.insert(tk.END, "Graph must have at least 2 nodes to find the largest connected component.\n")
        return
    
    largest_cc = max(nx.connected_components(G), key=len)
    subgraph = G.subgraph(largest_cc).copy()
    G.clear()
    G.add_edges_from(subgraph.edges)
    update_plot()
    log_text.insert(tk.END, "Truncated graph to its largest connected component.\n")

# Function to add the edge that maximizes algebraic connectivity by connecting the two most distant nodes
def add_max_distance_edge():
    if len(G.nodes) < 2:
        log_text.insert(tk.END, "Graph must have at least 2 nodes to add an edge.\n")
        return

    shortest_paths = dict(nx.all_pairs_shortest_path_length(G))
    max_distance = -1
    max_pair = None
    for u in G.nodes:
        for v in G.nodes:
            if u != v and (u, v) not in G.edges and (v, u) not in G.edges:
                if v in shortest_paths[u] and shortest_paths[u][v] > max_distance:
                    max_distance = shortest_paths[u][v]
                    max_pair = (u, v)

    if max_pair:
        u, v = max_pair
        initial_connectivity = algebraic_connectivity(G)
        G.add_edge(u, v)
        new_connectivity = algebraic_connectivity(G)
        update_plot()
        log_text.insert(tk.END, f"Added edge ({u}, {v}). Algebraic connectivity increased from {initial_connectivity:.4f} to {new_connectivity:.4f}.\n")
    else:
        log_text.insert(tk.END, "No suitable edge found to add.\n")

# Function to update the plot
def update_plot():
    ax.clear()
    pos = nx.spring_layout(G, dim=3)
    xs, ys, zs = zip(*[pos[n] for n in G.nodes])
    ax.scatter(xs, ys, zs, c='r', marker='o')
    for edge in G.edges:
        x = np.array([pos[edge[0]][0], pos[edge[1]][0]])
        y = np.array([pos[edge[0]][1], pos[edge[1]][1]])
        z = np.array([pos[edge[0]][2], pos[edge[1]][2]])
        ax.plot(x, y, z, c='b')
    canvas.draw()

# Initialize the main window
root = tk.Tk()
root.title("Graph Visualization and Algebraic Connectivity")

# Create a frame for inputs
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

# Entry for number of nodes and edges
ttk.Label(input_frame, text="Number of Nodes:").grid(row=0, column=0, padx=5, pady=5)
entry_nodes = ttk.Entry(input_frame, width=10)
entry_nodes.grid(row=0, column=1, padx=5, pady=5)
ttk.Label(input_frame, text="Number of Edges:").grid(row=0, column=2, padx=5, pady=5)
entry_edges = ttk.Entry(input_frame, width=10)
entry_edges.grid(row=0, column=3, padx=5, pady=5)

# Button frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Button to generate graph
button_generate = ttk.Button(button_frame, text="Generate Graph", command=generate_graph)
button_generate.grid(row=0, column=0, padx=5, pady=5)

# Button to constrain the graph to its minimal connected structure
button_constrain = ttk.Button(button_frame, text="Constrain to Minimal Connected Structure", command=constrain_to_minimal_connected_structure)
button_constrain.grid(row=0, column=1, padx=5, pady=5)

# Button to truncate the graph to its largest connected component
button_truncate = ttk.Button(button_frame, text="Truncate to Largest Component", command=truncate_to_largest_component)
button_truncate.grid(row=0, column=2, padx=5, pady=5)

# Button to add edge that maximizes algebraic connectivity by connecting the most distant nodes
button_add_edge = ttk.Button(button_frame, text="Add Max Distance Edge", command=add_max_distance_edge)
button_add_edge.grid(row=0, column=3, padx=5, pady=5)

# Matplotlib figure and canvas
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Text box for logs
log_text = tk.Text(root, height=10)
log_text.pack(pady=10)

# Initialize an empty graph
G = nx.Graph()

# Start the Tkinter event loop
root.mainloop()
