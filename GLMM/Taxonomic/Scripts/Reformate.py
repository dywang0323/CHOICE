# This script is used for selecting confifent taxonomic annotation from output of Kaiju, and just keep the useful columns

import os

def process_files(input_directory_path, output_directory_path):
    for filename in os.listdir(input_directory_path):
        # Check if the file is a text file
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_directory_path, filename)
            output_file_path = os.path.join(output_directory_path, filename)

            # Read and filter lines where the first column starts with "C"
            with open(input_file_path, 'r') as file:
                filtered_lines = [line for line in file if line.startswith('C')]

            # Remove the first column
            lines_without_first_column = ['\t'.join(line.split('\t')[1:]) for line in filtered_lines]

            # Save the processed lines to the new directory
            with open(output_file_path, 'w') as file:
                file.writelines(lines_without_first_column)

            print(f'Processed file saved: {output_file_path}')

# Specify your input and output directory paths here
input_directory_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Kaiju/Infant/TaxonNames/'
output_directory_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Kaiju/Infant/Taxa_name/'
process_files(input_directory_path, output_directory_path)
