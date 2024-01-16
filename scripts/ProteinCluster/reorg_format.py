import re

def parse_cluster_file(file_path):
    clusters = {}
    current_cluster = None

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('>Cluster'):
                current_cluster = line.split()[1]
                clusters[current_cluster] = []
            elif current_cluster is not None:
                match = re.search(r'>[^\s]+', line)
                if match:
                    sequence_id = match.group()[1:]  # Removing the leading '>'
                    sequence_id = sequence_id.replace('...', '')  # Removing '...'
                    clusters[current_cluster].append(sequence_id)

    return clusters

def format_clusters_to_string(clusters):
    formatted_output = ["clusterID\tProteins"]
    for cluster_id, proteins in clusters.items():
        formatted_output.append(f"Cluster_{cluster_id}\t{','.join(proteins)}")
    return '\n'.join(formatted_output)

def main():
    input_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Infant.clstr'  # Replace with your file path
    output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Fromated_Infant.clstr'  # Output file

    parsed_clusters = parse_cluster_file(input_file_path)
    formatted_output = format_clusters_to_string(parsed_clusters)

    # Write the formatted output to a file
    with open(output_file_path, 'w') as output_file:
        output_file.write(formatted_output)

    print(f"Formatted clusters have been saved to {output_file_path}")

if __name__ == "__main__":
    main()
