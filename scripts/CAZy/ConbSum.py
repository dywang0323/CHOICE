import os
import pandas as pd
import zipfile

# Define the path for the uploaded zip file and the extraction directory
zip_file_path = '/path/to/your/Combine.zip'
extraction_path = '/path/to/your/extraction/directory'

# Unzip the file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extraction_path)

# Change the directory path to the extracted 'Combine' folder
directory_path = os.path.join(extraction_path, 'Combine')

# Initialize an empty DataFrame to hold the combined data
combined_df = pd.DataFrame()

# List all the files in the directory
files = [file for file in os.listdir(directory_path) if file.endswith('.txt')]
files.sort()

# Iterate through each file and merge the data into the combined_df DataFrame
for file in files:
    file_path = os.path.join(directory_path, file)
    
    # Read the current file into a DataFrame
    current_df = pd.read_csv(file_path, sep='\t')
    
    # Check if the 'locus' column is unique within the current file
    if not current_df['locus'].is_unique:
        # If 'locus' is not unique, aggregate the data by 'locus'
        current_df = current_df.groupby('locus', as_index=False).agg('sum')
    
    # Extract the condition from the filename (e.g., M01_31 from M01_31.txt)
    condition = file.rstrip('.txt')
    
    # Rename the 'Sum_of_Peak_Heights' column to include the condition
    current_df.rename(columns={'Sum_of_Peak_Heights': f'Sum_of_Peak_Heights_{condition}'}, inplace=True)
    
    # If combined_df is empty, initialize it with the current_df
    if combined_df.empty:
        combined_df = current_df
    else:
        # Merge the current_df into the combined_df on 'locus'
        combined_df = pd.merge(combined_df, current_df, on='locus', how='outer')

# Fill NaN values with 0 after merging
combined_df.fillna(0, inplace=True)

# Define the output file path
output_file_path = '/path/to/your/output/CHOICEpro_B_CAZy.csv'

# Save the combined DataFrame to a CSV file
combined_df.to_csv(output_file_path, index=False)

# Print the path to the output file
print(f"Combined CSV file saved to: {output_file_path}")
