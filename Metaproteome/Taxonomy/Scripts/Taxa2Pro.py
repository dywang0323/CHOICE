# This script is used for organize the taxonic data into the following format:
# >species
# Scarfold_1
# Scarfold_2

from collections import defaultdict

# Replace 'input_file_path' with the path to your input file
input_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Kaiju/Infant/NAME_GENUS/Infant_Genus.txt'
# Replace 'output_file_path' with the path where you want to save the output file
output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Kaiju/Infant/NAME_GENUS/Genus_reform_infnat.txt'

def process_data(input_path, output_path):
    # Create a dictionary to hold the data
    data_dict = defaultdict(list)

    # Read the original data
    with open(input_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                identifier = parts[0]  # This is the unique sequence ID
                combined_id_name = f"{parts[1]}_{parts[2]}"  # This is the combined ID and name
                data_dict[combined_id_name].append(identifier)

    # Write the data into the new format
    with open(output_path, 'w') as processed_file:
        for combined_id_name, identifiers in data_dict.items():
            processed_file.write(f">{combined_id_name}\n")
            for identifier in identifiers:
                processed_file.write(f"{identifier}\n")

# Call the function with the input and output file paths
process_data(input_file_path, output_file_path)

print(f"Data has been processed and output to {output_file_path}")
