import os
import csv

def parse_protein_length_file(file_path):
    protein_lengths = {}
    total_length = 0
    count = 0
    with open(file_path, 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                protein_id, length_str = parts[0], parts[1]
                try:
                    length = int(length_str)
                    protein_lengths[protein_id] = length
                    total_length += length
                    count += 1
                except ValueError:
                    continue
    average_length = total_length / count if count > 0 else 0
    return protein_lengths, average_length

def calculate_and_scale_nsaf(peak_height_file, protein_lengths, average_length, scale_factor=1000000):
    nsaf_values = {}
    total = 0

    if average_length == 0:
        print("Warning: Average length is zero. This might lead to division by zero errors.")

    with open(peak_height_file, 'r') as file:
        next(file)  # Skip the first line (header)
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                protein_id = parts[0]
                try:
                    peak_height = float(parts[1])
                    length = protein_lengths.get(protein_id, average_length)
                    if length == 0:
                        print(f"Warning: Length for protein {protein_id} is zero. Using average length instead.")
                        length = average_length
                        if length == 0:
                            print("Error: Average length is also zero. Skipping this protein.")
                            continue
                    nsaf = peak_height / length
                    nsaf_values[protein_id] = nsaf
                    total += nsaf
                except ValueError as e:
                    print(f"Error processing line: {line}. Error: {e}")
                    continue

    for protein_id in nsaf_values:
        nsaf_values[protein_id] = (nsaf_values[protein_id] / total) * scale_factor
    return nsaf_values

def process_directory(peak_height_dir, protein_length_file, output_dir):
    print("Reading protein lengths...")
    protein_lengths, average_length = parse_protein_length_file(protein_length_file)
    print("Protein lengths read. Processing peak height files...")
    
    for peak_height_filename in os.listdir(peak_height_dir):
        print("Found file:", peak_height_filename)
        if peak_height_filename.endswith(".txt"):
            peak_height_file_path = os.path.join(peak_height_dir, peak_height_filename)
            nsaf_values = calculate_and_scale_nsaf(peak_height_file_path, protein_lengths, average_length)
            
            # Outputting NSAF values to a CSV file
            output_file_name = peak_height_filename.replace('.txt', '_NSAF.csv')
            output_file_path = os.path.join(output_dir, output_file_name)
            with open(output_file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Protein ID', 'NSAF Value'])
                for protein_id, nsaf_value in nsaf_values.items():
                    writer.writerow([protein_id, nsaf_value])
            
            print(f"NSAF values saved to {output_file_path}")
        else:
            print(f"Skipping file: {peak_height_filename} (does not end with '.txt')")

# Example usage
protein_length_file = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/CAZy/LengthCAZy.txt'  # Replace with your file path
peak_height_dir = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/CAZy/Infant_CAZy/Combine/'  # Replace with your directory path
output_dir = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/CAZy/NSAF_infant/'  # Replace with your output directory
process_directory(peak_height_dir, protein_length_file, output_dir)
