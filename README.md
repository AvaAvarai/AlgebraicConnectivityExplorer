# Algebraic Connectivity Explorer

This tool utilizes:

- `networkx` for graph creation and manipulation
- `matplotlib` for graph visualization
- `numpy` for numerical operations

Provides features of:

- Generating random graphs with a specified number of nodes and edges
- Visualizing the graph in a 3D space
- Constraining the graph to its minimal connected structure
- Truncating the graph to its largest connected component
- Adding an edge that maximizes the algebraic connectivity by connecting the two most distant nodes in terms of shortest path distance
- Logging actions and updates to the GUI window

## How to Use

1. Launch the Program
   - Run the Python script in your terminal or IDE. This will start the program and provide inputs.

2. Input Parameters
   - Number of Nodes: Enter the number of nodes for the graph in the text box "Number of Nodes".
   - Number of Edges: Enter the number of edges for the graph in the text box "Number of Edges".

3. Generate Graph
   - After entering the parameters, click the "Generate Graph" button. A random graph will be generated with the specified number of nodes and edges. The generated graph will be displayed in a 3D plot within the GUI window.

4. Constrain to Minimal Connected Structure
   - Click the "Constrain to Minimal Connected Structure" button. The graph will be constrained to its minimal connected structure, which will be displayed in the plot within the GUI window, and the console will log the changes.

5. Truncate to Largest Component
   - Click the "Truncate to Largest Component" button. The graph will be truncated to its largest connected component. The updated graph will be displayed in the plot within the GUI window, and the console will log the changes.

6. Add Edge to Maximize Algebraic Connectivity
   - Click the "Add Max Distance Edge" button. The program will attempt to add an edge that maximizes the algebraic connectivity by connecting the two most distant nodes. The updated graph will be displayed in the plot within the GUI window, and the console will log the changes.

## Example

1. Run the program:
   ```sh
   python graph_visualization.py
   ```
