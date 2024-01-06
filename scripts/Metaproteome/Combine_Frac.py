import pandas as pd
import glob

def process_dataframe(df, identifier):
    # Clean 'locus' column
    df['locus'] = df['locus'].apply(lambda x: x.split(',')[0].replace('{', '').replace('}', ''))
    
    # Rename the 'totalPeakHeight' column to include the identifier
    df.rename(columns={'totalPeakHeight': f'total_Peak_Height_{identifier}'}, inplace=True)

    # Retain only necessary columns
    df = df[['locus', 'description', f'total_Peak_Height_{identifier}']]
    return df

# Specify the path to your directory
path = '/scratch/dywang/Metaproteome_CAZy/M01_31_CAZy'

# Get a list of all files in the directory
files = glob.glob(path + '*.txt')
files.sort()

# Initialize final dataframe
final_df = pd.DataFrame()

for file in files:
    # Read the file, skipping the first row
    df = pd.read_csv(file, sep='\t', skiprows=1)

    # Extract identifier from filename (adjust this according to your filename pattern)
    identifier = file.split('/')[-1].split('.')[0]

    # Process the DataFrame
    df_processed = process_dataframe(df, identifier)

    # Merge with the final DataFrame
    if final_df.empty:
        final_df = df_processed
    else:
        final_df = pd.merge(final_df, df_processed, on=['locus', 'description'], how='outer')

# Add a column to calculate the sum of peak heights for each record
peak_height_columns = [col for col in final_df if col.startswith('total_Peak_Height')]
final_df['Sum_of_Peak_Heights'] = final_df[peak_height_columns].sum(axis=1)

# Keep 'locus', 'description', and 'Sum_of_Peak_Heights' columns
final_output_df = final_df[['locus', 'description', 'Sum_of_Peak_Heights']]

# Save the final DataFrame to a new text file
final_output_df.to_csv('merged_output_with_description.txt', sep='\t', index=False)
