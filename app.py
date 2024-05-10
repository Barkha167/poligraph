import streamlit as st
import subprocess
import os
import networkx as nx
import matplotlib.pyplot as plt

# Function to generate .graphml file from the provided URL
def generate_graphml(url):
    # Command to execute the provided commands
    commands = [
        f"python -m poligrapher.scripts.html_crawler {url} example/",
        "python -m poligrapher.scripts.init_document example/",
        "python -m poligrapher.scripts.run_annotators example/",
        "python -m poligrapher.scripts.build_graph example/",
        "python -m poligrapher.scripts.build_graph --pretty example/"
    ]
    
    # Execute commands
    for command in commands:
        subprocess.run(command, shell=True)

    # Return path of the generated .graphml file
    graphml_path = "example/graph-original.graphml"
    return graphml_path

# Function to load the graph from a GraphML file
def load_graph(file_path):
    try:
        G = nx.read_graphml(file_path)
        return G
    except Exception as e:
        st.error(f"Error loading the graph: {e}")
        return None

# Streamlit app
def main():
    st.title("PoliGraph: Automated Privacy Policy Analysis using Knowledge Graphs")

    # Text input for the URL
    url = st.text_input("Paste URL of Policy")

    # Define graphml_path
    graphml_path = None

    # Check if the URL is provided and the button is clicked
    if st.button("Create to .graphml file") and url:
        # Generate .graphml file
        graphml_path = generate_graphml(url)

        # Display success message
        st.success("GraphML file generated successfully!")
    
    # # Provide download link for the generated .graphml file
    # if graphml_path and os.path.exists(graphml_path):
    #     st.markdown(f'[Download .graphml file](example/graph-original.graphml)')

    # Load the graph if it exists
    if graphml_path and os.path.exists(graphml_path):
        graph = load_graph(graphml_path)
        if graph is not None:
            st.success("Graph loaded successfully!")

            # Display basic information about the graph
            st.subheader("Basic Information:")
            st.write(f"Number of nodes: {graph.number_of_nodes()}")
            st.write(f"Number of edges: {graph.number_of_edges()}")

            # Display node and edge attributes
            st.subheader("Node and Edge Attributes:")

            # Node attributes
            with st.expander("Node Attributes"):
                node_attributes = {node: data for node, data in graph.nodes(data=True)}
                st.write("Node attributes:", node_attributes)

            # Edge attributes
            with st.expander("Edge Attributes"):
                edge_attributes = {f"{u}-{v}": data for u, v, data in graph.edges(data=True)}
                st.write("Edge attributes:", edge_attributes)

            # Draw the graph
            st.subheader("Graph Visualization:")
            fig, ax = plt.subplots(figsize=(10, 8))
            pos = nx.spring_layout(graph)
            nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=10, ax=ax)
            edge_labels = nx.get_edge_attributes(graph, 'weight')
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
            plt.title('Graph Visualization')
            st.pyplot(fig)

# Run the app
if __name__ == "__main__":
    main()
