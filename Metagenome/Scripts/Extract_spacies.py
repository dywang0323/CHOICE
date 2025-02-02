# This script is used to extract records at the species level from the output of Metaphlan.

import pandas as pd

# Load the TSV file
file_path = "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/HUMANN/Maternal/Merge/Reactions_mother_norm.tsv"  # Replace with the actual file path
df = pd.read_csv(file_path, sep='\t', comment='#', dtype=str)  # Ignore lines starting with '#'

# Filter species-level records (7 taxonomic levels including the species level)
species_level_df = df[df['clade_name'].str.count(r'\|') == 6]

# Reset index to remove unnecessary numbered index column
species_level_df = species_level_df.reset_index(drop=True)

# Rename columns by removing "_metaphlan_bugs_list"
species_level_df.columns = species_level_df.columns.str.replace('_metaphlan_bugs_list', '', regex=True)

# Save the cleaned data to a new TSV file
output_file_path = "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/HUMANN/Maternal/Merge/Reactions_mother_species_norm.tsv"
species_level_df.to_csv(output_file_path, sep='\t', index=False)

print(f"Cleaned data saved to: {output_file_path}")
