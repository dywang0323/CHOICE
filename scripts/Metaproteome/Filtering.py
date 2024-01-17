import pandas as pd

# Load the CSV file
file_path = 'path_to_your_csv_file.csv'
data = pd.read_csv(file_path)

# Count the number of non-zero values in each row excluding the first column
non_zero_counts = (data.iloc[:, 1:] != 0).sum(axis=1)

# Filter out the rows where less than three columns have a non-zero value
filtered_data = data[non_zero_counts >= 3]

# Save the filtered data to a new CSV file
filtered_file_path = 'path_to_save_filtered_csv_file.csv'
filtered_data.to_csv(filtered_file_path, index=False)
