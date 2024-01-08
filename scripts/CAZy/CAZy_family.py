import pandas as pd

def process_and_consolidate_data(file_path, output_file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Creating a new DataFrame for the corrected data
    corrected_data = pd.DataFrame()

    # Iterate through each row in the original DataFrame
    for index, row in data.iterrows():
        # Splitting the family IDs and excluding the first part (before the first "|")
        family_ids = row['uniprot'].split('|')[1:]  # Skip the first part
        num_ids = len(family_ids)
        
        # Dividing the numerical values by the number of family IDs
        divided_values = row.drop('uniprot') / num_ids
        
        # Creating new rows for each family ID
        for fid in family_ids:
            new_row = divided_values.copy()
            new_row['uniprot'] = fid
            corrected_data = corrected_data.append(new_row, ignore_index=True)

    # Rearranging columns to match the original order
    column_order = data.columns.tolist()
    corrected_data = corrected_data[column_order]

    # Group by 'uniprot' and sum the numerical values
    consolidated_data = corrected_data.groupby('uniprot').sum().reset_index()

    # Save the consolidated DataFrame as a new CSV file
    consolidated_data.to_csv(output_file_path, index=False)

# Define the paths for the input and output files
file_path = 'path_to_your_input_file.csv'
output_file_path = 'path_to_your_output_file.csv'

# Process the data and consolidate
process_and_consolidate_data(file_path, output_file_path)
