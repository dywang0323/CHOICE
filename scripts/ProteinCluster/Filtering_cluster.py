# This script is used to filter clusters containing fewer than 10 subjects

from collections import defaultdict

# Function to extract the subject_ID from an entry
def extract_subject_id(entry):
    return entry[:6]

# File paths
input_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/ClusterPro_M.txt'  # Replace with your input file path
output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/ClusterPro_M_filtered.txt'  # Replace with your desired output file path

# Reading the file and storing the full IDs for each cluster
clusters = defaultdict(list)
with open(input_file_path, 'r') as file:
    for line in file:
        if line.startswith('>Cluster'):
            current_cluster = line.strip()
            clusters[current_cluster] = []
        else:
            clusters[current_cluster].append(line.strip())

# Filtering the clusters while keeping the full IDs
filtered_clusters = {cluster: full_ids for cluster, full_ids in clusters.items() 
                     if len(set(extract_subject_id(id) for id in full_ids)) >= 17}

# Writing the correctly filtered clusters to a text file
with open(output_file_path, 'w') as file:
    for cluster, full_ids in filtered_clusters.items():
        file.write(cluster + '\n')
        for full_id in full_ids:
            file.write(full_id + '\n')
