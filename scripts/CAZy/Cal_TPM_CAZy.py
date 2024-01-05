def extract_length(uniprot):
    match = re.search(r'(\d+)$', uniprot)
    return int(match.group(1)) if match else None

# Load the example data files
length_data = pd.read_csv('/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/LengthCAZy.txt', sep='\t')
count_data = pd.read_csv('/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/ReadMapping/CAZy_M/ReadCount_time/CHOICE_M_time.txt', sep='\t')


# Standardize and extract gene lengths from the 'uniprot' identifiers
length_data['uniprot'] = length_data['uniprot'].apply(lambda x: x.split(' ')[0])
length_data['Length'] = length_data['uniprot'].apply(extract_length)

# Merge the count data with the length data
merged_data = pd.merge(count_data, length_data, on='uniprot', how='left')

# Ensure only numeric columns are used for RPK calculation
numeric_cols = merged_data.select_dtypes(include=['number']).columns
merged_data_numeric = merged_data[numeric_cols]

# Calculate RPK
merged_data_numeric['Length_kb'] = merged_data['Length'] / 1000
merged_data_numeric['Length_kb'] = merged_data_numeric['Length_kb'].replace(0, 0.475)  # Avoid division by zero
rpk = merged_data_numeric.drop(['Length', 'Length_kb'], axis=1).div(merged_data_numeric['Length_kb'], axis=0)

# Calculate scaling factor and TPM
per_million = rpk.sum().sum() / 1_000_000
tpm = rpk / per_million * 1_000_000

# Replace non-finite values with zero and convert to integer
tpm_int = tpm.fillna(0).replace([float('inf'), -float('inf')], 0).astype(int)

# Reattach the 'uniprot' column and make it the first column
tpm_int['uniprot'] = merged_data['uniprot']
cols = ['uniprot'] + [col for col in tpm_int.columns if col != 'uniprot']
tpm_int = tpm_int[cols]

# Remove records where all TPM values are zero, excluding 'uniprot'
tpm_int_filtered = tpm_int[~(tpm_int.drop(columns=['uniprot']) == 0).all(axis=1)]

# Print first few rows of the final TPM data
print("\nFirst few rows of processed TPM data after removing zeros:")
print(tpm_int_filtered.head())

# Optionally, save the final TPM data to a file
tpm_int_filtered.to_csv('/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/ReadMapping/CAZy_M/ReadCount_time/TPM_CHOICE_M_CAZy.csv', sep='\t', index=False)
