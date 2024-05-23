# This script is used for consolidate the values in each column based on the Taxonomic name

import pandas as pd

def consolidate_cluster_values(input_file_path, output_file_path):
    # Load the dataset
    data = pd.read_csv(input_file_path)
    
    # Group the data by 'Cluster' and calculate the sum for each group
    cluster_sum = data.groupby('Taxa').sum()
    
    # Reset the index to turn 'Cluster' back into a column
    cluster_sum.reset_index(inplace=True)
    
    # Save the consolidated data to a CSV file
    cluster_sum.to_csv(output_file_path, index=False)
    
    print(f'Consolidated data has been saved to {output_file_path}')

# Example usage
input_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Overall/GLMM_taxa/Infant/Infant_taxa.csv'  # Replace with the path to your input CSV file
output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Overall/GLMM_taxa/Infant/Infant_taxa_Sum.csv'  # Replace with your desired output CSV file path

# Call the function with the paths
consolidate_cluster_values(input_file_path, output_file_path)
