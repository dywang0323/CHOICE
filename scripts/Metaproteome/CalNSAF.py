import os
import csv

def find_matching_protein_length_file(peak_height_filename, protein_length_dir):
    prefix = peak_height_filename[:6]  # Extract the first six characters
    for length_filename in os.listdir(protein_length_dir):
        if length_filename.startswith(prefix):
            return os.path.join(protein_length_dir, length_filename)
    return None

def parse_protein_length_file(file_path):
    protein_lengths = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                protein_id, length_str = parts[0], parts[1]
                length = int(length_str)
                protein_lengths[protein_id] = length
    return protein_lengths

def calculate_and_scale_nsaf(peak_height_file, protein_lengths, scale_factor=1000000):
    nsaf_values = {}
    total = 0
    with open(peak_height_file, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                protein_id = parts[0]
                peak_height = float(parts[1])
                if protein_id in protein_lengths:
                    length = protein_lengths[protein_id]
                    nsaf = peak_height / length
                    nsaf_values[protein_id] = nsaf
                    total += nsaf
    for protein_id in nsaf_values:
        nsaf_values[protein_id] = (nsaf_values[protein_id] / total) * scale_factor
    return nsaf_values

def process_directory(peak_height_dir, protein_length_dir, output_dir):
    for peak_height_filename in os.listdir(peak_height_dir):
        if peak_height_filename.endswith("_modified.txt"):
            peak_height_file_path = os.path.join(peak_height_dir, peak_height_filename)
            protein_length_file_path = find_matching_protein_length_file(peak_height_filename, protein_length_dir)
            if protein_length_file_path:
                protein_lengths = parse_protein_length_file(protein_length_file_path)
                nsaf_values = calculate_and_scale_nsaf(peak_height_file_path, protein_lengths)
                
                # Outputting NSAF values to a CSV file
                output_file_name = peak_height_filename.replace('_modified.txt', '_NSAF.csv')
                output_file_path = os.path.join(output_dir, output_file_name)
                with open(output_file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Protein ID', 'NSAF Value'])
                    for protein_id, nsaf_value in nsaf_values.items():
                        writer.writerow([protein_id, nsaf_value])
                
                print(f"NSAF values saved to {output_file_path}")
            else:
                print(f"No matching protein length file found for {peak_height_filename}")

# Example usage
protein_length_dir = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/Length_B/'
peak_height_dir = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Overall/Modified_infant/'
output_dir = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Overall/NSAF_infant/'
process_directory(peak_height_dir, protein_length_dir, output_dir)
