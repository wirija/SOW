import os

import poutyne

from deepparse import download_from_public_repository
from deepparse.dataset_container import CSVDatasetContainer
from deepparse.parser import AddressParser

# First, let's download the train and test data from the public repository but using a CSV format dataset.
saving_dir = "./data"
file_extension = "csv"
training_dataset_name = "sample_incomplete_data"
test_dataset_name = "test_sample_data"
download_from_public_repository(training_dataset_name, saving_dir, file_extension=file_extension)
download_from_public_repository(test_dataset_name, saving_dir, file_extension=file_extension)

# Now let's create a training and test container.
training_container = CSVDatasetContainer(
    os.path.join(saving_dir, training_dataset_name + "." + file_extension),
    column_names=["Address", "Tags"],
    separator=",",
)
test_container = CSVDatasetContainer(
    os.path.join(saving_dir, test_dataset_name + "." + file_extension),
    column_names=["Address", "Tags"],
    separator=",",
)

# We will retrain the FastText version of our pretrained model.
address_parser = AddressParser(model_type="fasttext", device=0)

# Now, let's retrain for 5 epochs using a batch size of 8 since the data is really small for the example.
# Let's start with the default learning rate of 0.01 and use a learning rate scheduler to lower the learning rate
# as we progress.
lr_scheduler = poutyne.StepLR(step_size=1, gamma=0.1)  # reduce LR by a factor of 10 each epoch

# The checkpoints (ckpt) are saved in the default "./checkpoints" directory, so if you wish to retrain
# another model (let's say BPEmb), you need to change the `logging_path` directory; otherwise, you will get
# an error when retraining since Poutyne will try to use the last checkpoint.
address_parser.retrain(
    training_container,
    train_ratio=0.8,
    epochs=5,
    batch_size=8,
    num_workers=2,
    callbacks=[lr_scheduler],
)

# Now, let's test our fine-tuned model using the best checkpoint (default parameter).
address_parser.test(test_container, batch_size=256)

# Now let's retrain the FastText version but with an attention mechanism.
address_parser = AddressParser(model_type="fasttext", device=0, attention_mechanism=True)

# Since the previous checkpoints were saved in the default "./checkpoints" directory, we need to use a new one.
# Otherwise, poutyne will try to reload the previous checkpoints, and our model has changed.
address_parser.retrain(
    training_container,
    train_ratio=0.8,
    epochs=5,
    batch_size=8,
    num_workers=2,
    callbacks=[lr_scheduler],
    logging_path="checkpoints_attention",
)

# Now, let's test our fine-tuned model using the best checkpoint (default parameter).
address_parser.test(test_container, batch_size=256)





# import os
# from grape import Graph

# # Re-create a simple edges.csv for demonstration
# # edges_content = "source,destination\nNodeA,NodeB\nNodeB,NodeC\nNodeC,NodeA\nNodeD,NodeE"
# # with open("edges.csv", "w") as f:
# #     f.write(edges_content)
# # print("Created 'edges.csv' for centrality demonstration.")

# # Load the graph (let's keep it undirected for common centrality measures)
# try:
#     # graph = Graph.from_csv(
#     #     edge_path="edges.csv",
#     #     directed=False,
#     #     name="CentralityGraph"
#     # )



#     graph = Graph.from_csv(
#             node_path="nodes.csv", 
#             nodes_column="Nodes",
#             node_list_node_types_column="NodeType",
#             node_list_separator = "|",
#             # node_list_node_types_column=const.COL_NODE_TYPE,

#             edge_path="edges.csv",
#             edge_list_separator = "|",
#             sources_column="source",
#             destinations_column="destination",
#             edge_list_support_balanced_quotes = True,

#             directed=False,
#             name="Group Graph"
#         )
            
#     # print(f"Graph '{graph.get_name()}' loaded successfully.")
#     # print(f"Number of nodes: {graph.get_nodes_number()}")
#     # print(f"Number of edges: {graph.get_edges_number()}")
# except Exception as e:
#     print(f"Error loading graph: {e}")
#     exit()

# connected_components_ids = graph.get_connected_components()





# print (graph.get_node_type_ids())




# for node, group_id in zip(list(graph.get_node_names()), list(connected_components_ids[0])):
#     print (f"{node}, {group_id}")


# # print("\n--- Connected Components ---")
# # for node_id, group_id in enumerate(connected_components_ids):
# #     node_name = node_id_to_name[node_id]
# #     print(f'"{node_name}", :{group_id}')

# # components_map = {}
# # for node_id, group_id in enumerate(connected_components_ids):
# #     node_name = node_id_to_name[node_id]
# #     if group_id not in components_map:
# #         components_map[group_id] = []
# #     components_map[group_id].append(node_name)

# # print("\n--- Connected Components Grouped ---")
# # for group_id, nodes in components_map.items():
# #     print(f"Group {group_id}: {', '.join(nodes)}")
# #         return


# """"

# # Get a mapping from internal node ID to node name for output
# node_id_to_name = graph.get_node_names()

# print("\n--- Centrality Measures ---")

# # --- 2.1. Degree Centrality ---
# # Measures the number of direct connections a node has.
# # For undirected graphs, in_degree and out_degree are the same.
# # For directed graphs, you can get in_degree or out_degree separately.
# print("\n--- Degree Centrality ---")
# try:
#     # `get_degree()` returns the total degree for undirected graphs
#     # or the out-degree for directed graphs by default.
#     # Use `get_in_degree()` for in-degree on directed graphs.
#     degrees = graph.get_degree()
#     for node_id, score in enumerate(degrees):
#         node_name = node_id_to_name[node_id]
#         print(f'"{node_name}", Degree: {score}')
# except Exception as e:
#     print(f"Error calculating Degree Centrality: {e}")

# # --- 2.2. Betweenness Centrality ---
# # Measures the extent to which a node lies on shortest paths between other nodes.
# # Can be computationally expensive for large graphs.
# print("\n--- Betweenness Centrality ---")
# try:
#     # The `verbose=True` parameter will show a progress bar if enabled globally
#     # or for this specific call.
#     betweenness_scores = graph.get_betweenness_centrality(verbose=True)
#     for node_id, score in enumerate(betweenness_scores):
#         node_name = node_id_to_name[node_id]
#         print(f'"{node_name}", Betweenness: {score:.4f}')
# except Exception as e:
#     print(f"Error calculating Betweenness Centrality: {e}")


# # --- 2.3. Closeness Centrality ---
# # Measures how close a node is to all other nodes in the network.
# # Defined as the reciprocal of the sum of the shortest path distances from a node
# # to all other nodes. For disconnected graphs, it's typically undefined or 0.
# print("\n--- Closeness Centrality ---")
# try:
#     # For disconnected graphs, Closeness Centrality can be problematic.
#     # GRAPE handles this, often returning 0 for nodes in isolated components.
#     closeness_scores = graph.get_closeness_centrality(verbose=True)
#     for node_id, score in enumerate(closeness_scores):
#         node_name = node_id_to_name[node_id]
#         print(f'"{node_name}", Closeness: {score:.4f}')
# except Exception as e:
#     print(f"Error calculating Closeness Centrality: {e}")


# # --- 2.4. Eigenvector Centrality ---
# # Measures the influence of a node in a network.
# # It assigns relative scores to all nodes in the network based on the concept
# # that connections to high-scoring nodes contribute more to the score of the node in question.
# print("\n--- Eigenvector Centrality ---")
# try:
#     # Requires a converged algorithm (like power iteration)
#     eigenvector_scores = graph.get_eigenvector_centrality(verbose=True)
#     for node_id, score in enumerate(eigenvector_scores):
#         node_name = node_id_to_name[node_id]
#         print(f'"{node_name}", Eigenvector: {score:.4f}')
# except Exception as e:
#     print(f"Error calculating Eigenvector Centrality: {e}")


# # --- 2.5. PageRank (Similar to Eigenvector Centrality for directed graphs) ---
# # While primarily for directed graphs (web pages), it can be applied to undirected too.
# # Measures the importance of a node by considering the importance of its neighbors.
# print("\n--- PageRank (for comparison) ---")
# try:
#     # For undirected graphs, PageRank often yields similar results to Eigenvector Centrality,
#     # but it's fundamentally designed for directed links.
#     # You might want to set a damping factor (default is often 0.85)
#     pagerank_scores = graph.get_pagerank(verbose=True)
#     for node_id, score in enumerate(pagerank_scores):
#         node_name = node_id_to_name[node_id]
#         print(f'"{node_name}", PageRank: {score:.4f}')
# except Exception as e:
#     print(f"Error calculating PageRank: {e}")


# # Clean up the dummy file
# if os.path.exists("edges.csv"):
#     os.remove("edges.csv")
# print("\nCleaned up 'edges.csv'.")


# # Get connected components
# connected_components_ids = graph.get_connected_components()

# print("\n--- Connected Components ---")
# for node_id, group_id in enumerate(connected_components_ids):
#     node_name = node_id_to_name[node_id]
#     print(f'"{node_name}", :{group_id}')

# components_map = {}
# for node_id, group_id in enumerate(connected_components_ids):
#     node_name = node_id_to_name[node_id]
#     if group_id not in components_map:
#         components_map[group_id] = []
#     components_map[group_id].append(node_name)

# print("\n--- Connected Components Grouped ---")
# for group_id, nodes in components_map.items():
#     print(f"Group {group_id}: {', '.join(nodes)}")

# """



# # from grape import Graph

# # # A list of node names you want in your graph
# # node_names_list = ["NodeA", "NodeB", "NodeC", "NodeD", "NodeE"]

# # # Create a graph from these node names
# # # This is like "adding" nodes to an empty graph
# # graph_from_names = Graph.from_node_names(
# #     node_names=node_names_list,
# #     directed=False, # Or True
# #     name="MyNodesOnlyGraph"
# # )

# # print(f"Graph '{graph_from_names.get_name()}' created from node names.")
# # print(f"Number of nodes: {graph_from_names.get_nodes_number()}")
# # print(f"Nodes: {graph_from_names.get_node_names()}")
# # print(f"Number of edges: {graph_from_names.get_edges_number()}") # Will be 0