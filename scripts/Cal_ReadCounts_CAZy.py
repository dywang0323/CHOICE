import os
import pandas as pd

# Specify the path to your directory
path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/ReadMapping/CAZy_M/ReadCount_time/'

# Get a list of all files in the directory
files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

# Initialize the final DataFrame with 'uniprot' as the index
final_df = pd.DataFrame()

# Loop through all files and merge them on the 'uniprot' column
for file in files:
    file_path = os.path.join(path, file)
    identifier = file.split('_')[0]
    
    # Check if the file is not a directory and has no extension
    if not os.path.isdir(file_path) and '.' not in file:
        df = pd.read_csv(file_path, sep='\t', comment='#')
        df = df.rename(columns={'COUNT': f'COUNT_{identifier}'})
        
        if final_df.empty:
            final_df = df
        else:
            final_df = final_df.merge(df, on='uniprot', how='outer')

# Replace missing values with 0
final_df.fillna(0, inplace=True)

# Save the final DataFrame to a new text file
final_df.to_csv('CHOICE_M_time.txt', sep='\t', index=False)
