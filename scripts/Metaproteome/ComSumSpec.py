#!/usr/bin/env python3
import pandas as pd
import os

# Directory containing the files
directory_path = '/path/to/your/directory'

# List to store dataframes
dataframes = []

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory_path, filename)
        df = pd.read_csv(file_path, sep='\t')
        column_name = 'Sum_of_Peak_Heights_' + filename.split('.')[0]
        df.rename(columns={'Sum_of_Peak_Heights': column_name}, inplace=True)
        dataframes.append(df)

# Merging all dataframes on the 'locus' column
combined_df = dataframes[0]
for df in dataframes[1:]:
    combined_df = combined_df.merge(df, on='locus', how='outer')

combined_df.fillna(0, inplace=True)
output_file_path = '/path/to/output/combined_data.csv'
combined_df.to_csv(output_file_path, index=False)
