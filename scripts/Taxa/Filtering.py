import pandas as pd

# Load the CSV file
file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/metaphlan/Species/2month_CHOICE.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Counting the number of non-zero values in each row (excluding the 'clade_name' column)
non_zero_counts = data.drop(columns=['clade_name']).ne(0).sum(axis=1)

# Filtering the dataframe to keep rows with 3 or more non-zero values
filtered_data = data[non_zero_counts >= 3]

# Define the path for the new filtered CSV file
filtered_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/metaphlan/Species/selected/2month_CHOICE.csv'  # Replace with your desired file path

# Save the filtered data to a new CSV file
filtered_data.to_csv(filtered_file_path, index=False)
