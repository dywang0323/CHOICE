# This script is used for format the input of GLMM analysis, including transpose, add the subject_ID column

import pandas as pd

def transpose_and_save_csv(input_file_path, output_file_path):
    # Load the data from the CSV file
    data = pd.read_csv(input_file_path)

    # Transposing the dataset
    transposed_data = data.set_index('Cluster').T

    # Resetting the index to turn it into a column and renaming it to 'Sample_ID'
    transposed_data_reset_index = transposed_data.reset_index().rename(columns={'index': 'Sample_ID'})

    # Extracting the first six characters from the 'Sample_ID' column to create 'Subject_ID'
    transposed_data_reset_index['Subject_ID'] = transposed_data_reset_index['Sample_ID'].str[:6]

    # Reordering columns to place 'Subject_ID' as the first column and 'Sample_ID' as the second
    column_order = ['Subject_ID', 'Sample_ID'] + [col for col in transposed_data_reset_index.columns if col not in ['Subject_ID', 'Sample_ID']]
    reordered_data = transposed_data_reset_index[column_order]

    # Saving the reordered data to a CSV file
    reordered_data.to_csv(output_file_path, index=False)

# Example usage
input_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Infant_Cluster_sum.csv'  # Replace with your input file path
output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Infant_Cluster_glmm.csv'  # Replace with your desired output file path

transpose_and_save_csv(input_file_path, output_file_path)
