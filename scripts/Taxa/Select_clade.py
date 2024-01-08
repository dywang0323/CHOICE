import pandas as pd

# Function to extract the specific substring
def extract_specific_substring(clade_name):
    if 's__' in clade_name:
        return clade_name.split('s__')[-1].split('|')[0]
    return None

# Load the dataset from a .txt file
file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/metaphlan/Maternal/merged_maternal_table.txt'  # Replace with your file path
# Adjust read_csv parameters as needed (like sep, header, etc.)
data = pd.read_csv(file_path, sep='\t', header=None)  # Assuming tab-separated values

# Assuming the first column contains the 'clade_name', replace '0' with the correct column index if different
data.columns = ['clade_name'] + [f'column_{i}' for i in range(1, len(data.columns))]

# Filter and modify the dataset
data_with_s = data[data['clade_name'].str.contains("s__")]
data_with_s['clade_name'] = data_with_s['clade_name'].apply(extract_specific_substring)

# Save the newly modified dataset to a CSV file
output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/metaphlan/Maternal/Species.csv'  # Replace with your desired output path
data_with_s.to_csv(output_file_path, index=False)
