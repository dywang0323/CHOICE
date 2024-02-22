# This script is used for annotating cluster

from collections import Counter
import csv

# Function to get the most common KO number and annotation for each cluster
def get_most_common_ko_annotation(records):
    # Extract the KO numbers and annotations
    ko_numbers = [record.split()[1] for record in records]
    annotations = [" ".join(record.split()[2:]) for record in records]

    # Find the most common KO number and corresponding annotation
    most_common_ko = Counter(ko_numbers).most_common(1)[0][0]
    # Find the annotation corresponding to the most common KO number
    most_common_annotation = next((ann for ko, ann in zip(ko_numbers, annotations) if ko == most_common_ko), "")
    
    return most_common_ko, most_common_annotation

# Function to process the text file and extract clusters and their records
def process_text_file(file_path):
    clusters = {}
    current_cluster = ""

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('>Cluster'):
                current_cluster = line.strip()
                clusters[current_cluster] = []
            elif "K" in line:
                clusters[current_cluster].append(line.strip())

    return clusters

# Define the path to the input text file
input_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/Annotation/ClusterPro_M_KO.txt'  # Replace with your actual file path

# Process the file to extract clusters and their records
clusters = process_text_file(input_file_path)

# Iterate through the clusters to format the data
formatted_data = []
for cluster_id, records in clusters.items():
    if records:
        ko_number, annotation = get_most_common_ko_annotation(records)
        formatted_data.append((cluster_id.replace('>', ''), ko_number, annotation))

# Write the formatted data to a CSV file
output_csv_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/Annotation/ClusterPro_M_KO_filtered.csv'  # Replace with your desired output file path
with open(output_csv_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Cluster', 'KO Number', 'Annotation'])  # Write header
    for row in formatted_data:
        csv_writer.writerow(row)  # Write the cluster data
