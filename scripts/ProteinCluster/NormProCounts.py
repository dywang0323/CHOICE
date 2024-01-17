import os
import pandas as pd

def extract_scaff_length(identifier):
    try:
        return int(identifier.split('_')[4])  # Adjust if necessary
    except (IndexError, ValueError):
        return None

def find_length_file(subject_name, length_dir):
    # Construct the expected length file name based on the subject name
    for file in os.listdir(length_dir):
        if subject_name in file:
            return os.path.join(length_dir, file)
    return None

def process_files(count_file, length_file, output_dir):
    # Reading files
    df_counts = pd.read_csv(count_file, sep=' ', header=None, names=['identifier', 'additional_info', 'protein_count'])
    df_lengths = pd.read_csv(length_file, sep='\t', header=None, names=['identifier', 'protein_length'])

    # Adjusting identifiers and merging
    df_lengths['adjusted_identifier'] = df_lengths['identifier'].apply(lambda x: '_'.join(x.split('_')[:-1]))
    df_merged = pd.merge(df_lengths, df_counts, left_on='adjusted_identifier', right_on='identifier', how='left')

    # Calculating normalized protein count
    df_merged['scaff_length'] = df_merged['identifier_x'].apply(extract_scaff_length)
    df_merged['normalized_count'] = (df_merged['protein_count'] / df_merged['scaff_length']) * df_merged['protein_length']

    # Constructing the output filename
    base_name = os.path.basename(count_file)
    output_filename = base_name.replace('_modified.counted', '') + '_normalized.csv'
    output_path = os.path.join(output_dir, output_filename)

    # Saving to CSV
    df_merged[['identifier_x', 'normalized_count']].to_csv(output_path, index=False)
    print(f"Saved to {output_path}")

def main():
    count_dir = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/ReadCounts/Modified_infant'  # Replace with your count files directory
    length_dir = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/Length_B'  # Replace with your length files directory
    output_dir = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/Norm_ProteinCounts/Infant'  # Replace with your desired output directory

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each count file
    for count_file in os.listdir(count_dir):
        subject_name = count_file[:6]  # Extracting the first six characters as the subject name
        length_file = find_length_file(subject_name, length_dir)

        if length_file:
            process_files(os.path.join(count_dir, count_file), length_file, output_dir)
        else:
            print(f"No matching length file found for {count_file}")

if __name__ == "__main__":
    main()
