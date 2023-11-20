import os
import pandas as pd

def process_cho01b(file_path):
    try:
        data = []
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) > 1:
                    id = '_'.join(parts[0].split('_')[:-1])  # Adjusting the ID format
                    code = parts[1]
                    data.append([id, code])
        return pd.DataFrame(data, columns=['ID', 'Code'])
    except Exception as e:
        print(f"Error processing CHO01B-like file {file_path}: {e}")
        return pd.DataFrame(columns=['ID', 'Code'])  # Return empty DataFrame in case of error

def process_counted_result(file_path):
    try:
        data = []
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 2:
                    id = parts[0]
                    try:
                        value = float(parts[-1])  # Convert to float
                    except ValueError:
                        continue  # Skip lines where the value is not a number
                    data.append([id, value])
        return pd.DataFrame(data, columns=['ID', 'Value'])
    except Exception as e:
        print(f"Error processing counted result file {file_path}: {e}")
        return pd.DataFrame(columns=['ID', 'Value'])  # Return empty DataFrame in case of error

def find_matching_file(base_name, directory):
    try:
        for filename in os.listdir(directory):
            if filename.startswith(base_name):
                return os.path.join(directory, filename)
        print(f"No matching file found for {base_name} in {directory}")
        return None
    except Exception as e:
        print(f"Error searching for matching file for {base_name} in {directory}: {e}")
        return None

def process_files(directory_cho01b, directory_counted_result, output_directory):
    try:
        for filename in os.listdir(directory_cho01b):
            if filename.endswith(".txt"):  # Adjust as needed
                base_name = os.path.splitext(filename)[0]
                print(f"Processing {base_name}...")
                cho01b_file_path = os.path.join(directory_cho01b, filename)
                counted_result_file_path = find_matching_file(base_name, directory_counted_result)

                if counted_result_file_path:
                    df_cho01b = process_cho01b(cho01b_file_path)
                    df_counted_result = process_counted_result(counted_result_file_path)

                    if not df_cho01b.empty and not df_counted_result.empty:
                        # Merging and consolidating
                        merged_df = pd.merge(df_cho01b, df_counted_result, on='ID', how='inner')
                        consolidated_df = merged_df.drop(columns=['ID']).groupby('Code').sum().reset_index()

                        # Save to CSV in the specified output directory
                        output_csv_path = os.path.join(output_directory, f'consolidated_{base_name}.csv')
                        consolidated_df.to_csv(output_csv_path, index=False)
                        print(f"Consolidated data saved to {output_csv_path}")
                else:
                    print(f"No corresponding counted result file found for {cho01b_file_path}")
            else:
                print(f"Skipping non-txt file {filename} in CHO01B-like directory")
    except Exception as e:
        print(f"General error in processing directories: {e}")

# Provide the paths to your directories here
directory_cho01b = '/work/TEDDY/DW/CHOICE/KO_fam_B'  # Replace with the path to the directory containing CHO01B.txt-like files
directory_counted_result = '/work/TEDDY/DW/CHOICE/RPKM_scaffold/read_counted_B'  # Replace with the path to the directory containing CHO01B.counted.result-like files
output_directory = '/work/TEDDY/DW/CHOICE/Infant_KO'  # Replace with the path to the directory where you want to save the output files

# Process the files
process_files(directory_cho01b, directory_counted_result, output_directory)
