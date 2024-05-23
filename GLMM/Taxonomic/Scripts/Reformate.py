# This script is used for selecting confifent taxonomic annotation from output of Kaiju, and just keep the useful columns

import os
import re

def process_files(input_directory_path, output_directory_path):
    # Check if the input directory exists
    if not os.path.isdir(input_directory_path):
        print(f"Input directory does not exist: {input_directory_path}")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory_path, exist_ok=True)

    # Define a regex pattern for species-level annotations
    species_level_pattern = re.compile(r'^[A-Za-z]+\s+[A-Za-z]+$')

    # Iterate over all files in the input directory
    for filename in os.listdir(input_directory_path):
        # Check if the file is a text file
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_directory_path, filename)
            output_file_path = os.path.join(output_directory_path, filename)

            try:
                # Read and filter lines where the first column starts with "C"
                with open(input_file_path, 'r') as file:
                    filtered_lines = [line for line in file if line.startswith('C')]

                # Remove the first column and keep records annotated at species level
                processed_lines = []
                for line in filtered_lines:
                    columns = line.split('\t')
                    annotation = columns[3].strip()  # Get the third column (species/genus annotation)
                    if species_level_pattern.match(annotation):
                        processed_lines.append('\t'.join(columns[1:]))

                # Write the processed lines to the output file
                with open(output_file_path, 'w') as file:
                    file.writelines(processed_lines)

                print(f'Processed file saved: {output_file_path}')

            except Exception as e:
                print(f"Error processing file {filename}: {e}")

# Specify your input and output directory paths here
input_directory_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Kaiju/Infant/TaxonNames/'
output_directory_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Taxanomic/Infant/TaxonomicName/'

process_files(input_directory_path, output_directory_path)
