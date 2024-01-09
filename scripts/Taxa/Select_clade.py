import pandas as pd

# Load the dataset from the text file
file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/metaphlan/Maternal/merged_maternal_table.txt'

# Load the data with tab as the delimiter and handling commented lines
data = pd.read_csv(file_path, delimiter='\t', comment='#')

# Print the column names to check them
print("Column names:", data.columns)

# Replace 'clade_name' with the actual column name from your data, if different
column_name = 'clade_name'  # Update this to the actual column name

# Filter the data for records where the specified column ends with 's__' followed by more characters
filtered_data = data[data[column_name].str.contains('s__[^|]*$')]

# Modify the column to keep only the part after 's__'
filtered_data[column_name] = filtered_data[column_name].str.extract('s__(.*)')

# Save the modified data to a CSV file
output_csv_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/metaphlan/Maternal/species.csv'
filtered_data.to_csv(output_csv_path, index=False)

print("Filtered data saved to:", output_csv_path)
