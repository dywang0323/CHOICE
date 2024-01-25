# This script is used for sum up values of each column within one cluster

import pandas as pd

def summarize_and_save_csv(input_file_path, output_file_path):
    # Load the data from the CSV file
    data = pd.read_csv(input_file_path)

    # Summing up the values for each column within each cluster
    cluster_sums = data.groupby('Cluster').sum()

    # Removing "_normalized" from the column headers
    cluster_sums.columns = [col.replace('_normalized', '') for col in cluster_sums.columns]

    # Saving the summarized data to a CSV file
    cluster_sums.to_csv(output_file_path)

# Example usage
input_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Materal_Cluster.csv'  # Replace with your input file path
output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Materal_Cluster_sum.csv'  # Replace with your desired output file path

summarize_and_save_csv(input_file_path, output_file_path)
