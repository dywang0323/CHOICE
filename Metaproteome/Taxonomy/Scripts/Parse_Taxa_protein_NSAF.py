# This script is used for parsing the taxonomic annoation from Kaiju with the NSAF value from metaproteomics

import pandas as pd
import os

# Function to parse the updated taxa/cluster file
def parse_taxa_file(taxa_file_path):
    taxa_data = {}
    taxa_ids = []
    taxa_labels = []
    with open(taxa_file_path, 'r') as file:
        current_taxa = ''
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                current_taxa = line[1:]
            else:
                taxa_ids.append(line)
                taxa_labels.append(current_taxa)
    return pd.DataFrame({'Taxa': taxa_labels}, index=taxa_ids)

# Function to read and merge CSV files
def merge_csv_files(csv_directory, taxa_df):
    for filename in os.listdir(csv_directory):
        if filename.endswith('_NSAF.csv'):
            # Extract the desired part of the filename
            column_name = filename.rsplit('_NSAF.csv', 1)[0]
            csv_path = os.path.join(csv_directory, filename)
            csv_data = pd.read_csv(csv_path)
            csv_data.set_index('Protein ID', inplace=True)
            csv_data.rename(columns={'NSAF Value': column_name}, inplace=True)
            taxa_df = pd.concat([taxa_df, csv_data], axis=1, join='outer')
    taxa_df.fillna(0, inplace=True)
    return taxa_df

# Main function to create the new merged file
def create_merged_file(taxa_file_path, csv_directory, output_file_path):
    taxa_df = parse_taxa_file(taxa_file_path)
    merged_data = merge_csv_files(csv_directory, taxa_df)
    # Ensuring 'Taxa' is the first column
    merged_data = merged_data.reset_index().rename(columns={'index': 'Protein ID'})
    column_order = ['Taxa', 'Protein ID'] + [col for col in merged_data.columns if col not in ['Taxa', 'Protein ID']]
    merged_data = merged_data[column_order]
    merged_data.to_csv(output_file_path, index=False)

# Example usage
taxa_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Kaiju/Infant/NAME_GENUS/Genus_reform_infnat.txt'
csv_directory = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Overall/GLMM_NSAF/NSAF_infant/'
output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Kaiju/Infant/Kaiju_GENUS_PRO_Infant.csv'
create_merged_file(taxa_file_path, csv_directory, output_file_path)
