import os
import pandas as pd

def combine_csv_files(directory_path):
    all_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):  # Only process CSV files
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path)

            # Assuming the first column is KO ID and the second column is the value
            if df.shape[1] >= 2:
                df = df.iloc[:, :2]  # Only keep the first two columns
                df.columns = ['KO ID', os.path.splitext(filename)[0]]  # Rename columns
                all_data.append(df)

    # Merge all dataframes on KO ID
    combined_df = pd.DataFrame()
    for data in all_data:
        if combined_df.empty:
            combined_df = data
        else:
            combined_df = pd.merge(combined_df, data, on='KO ID', how='outer')

    return combined_df

# Replace with the path to the directory containing your CSV files
directory_path = '/work/TEDDY/DW/CHOICE/Infant_KO'

# Combine the files
combined_df = combine_csv_files(directory_path)

# Provide the path to the output directory here
output_directory = '/work/TEDDY/DW/CHOICE/Infant_KO'  # Replace with the path where you want to save the output file

# Save the combined data to a new CSV in the output directory
output_csv_path = os.path.join(output_directory, 'combined_data.csv')
combined_df.to_csv(output_csv_path, index=False)

print(f"Combined data saved to {output_csv_path}")
