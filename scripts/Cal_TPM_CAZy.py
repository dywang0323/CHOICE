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
merged_data_numeric['Length_kb'] = merged_data_numeric['Length_kb'].replace(0, 0.001)  # Avoid division by zero
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
