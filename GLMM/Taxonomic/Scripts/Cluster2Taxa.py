# This script is used for combine the taxonomic name and protein cluster file

import os

def read_info_files(directory_path):
    """Reads information from all txt files in the specified directory and creates a mapping."""
    mapping = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Adjust based on your files
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split('\t')
                    if len(parts) >= 3:
                        node_id, info1, info2 = parts[0], parts[1], parts[2]
                        if node_id not in mapping:
                            mapping[node_id] = set()
                        mapping[node_id].add((info1, info2))
    return mapping

def merge_cluster_info(cluster_file_path, mapping, output_file_path):
    """Merges the cluster file with the information from the mapping, omitting node IDs."""
    with open(cluster_file_path, 'r') as cluster_file, open(output_file_path, 'w') as merged_file:
        cluster_info = set()  # To track unique info for the current cluster
        for line in cluster_file:
            if line.startswith('>'):
                # If moving to a new cluster, write the previous cluster's info
                if cluster_info:
                    # Format aggregated info
                    formatted_info = ', '.join([f"{info[0]} {info[1]}" for info in cluster_info])
                    merged_file.write(f"{current_cluster}\t{formatted_info}\n")
                # Reset for the new cluster
                cluster_info = set()
                current_cluster = line.strip()
            else:
                node_id = line.strip()
                # Aggregate unique info for the current cluster
                if node_id in mapping:
                    cluster_info |= mapping[node_id]
        
        # Don't forget the last cluster's info
        if cluster_info:
            formatted_info = ', '.join([f"{info[0]} {info[1]}" for info in cluster_info])
            merged_file.write(f"{current_cluster}\t{formatted_info}\n")

# Setup your paths
directory_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Kaiju/Maternal/Taxa_name/'  # Directory containing files like CHO01B.txt
cluster_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/ClusterPro_M_filtered.txt'  # Adjust as necessary
output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/ClusterPro_M_Taxa.txt'  # Output file path

# Execute the process
mapping = read_info_files(directory_path)
merge_cluster_info(cluster_file_path, mapping, output_file_path)

print(f"Merged file with unique cluster information saved to {output_file_path}")
