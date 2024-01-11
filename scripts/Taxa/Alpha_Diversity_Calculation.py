import pandas as pd
from scipy.stats import entropy
import numpy as np

def calculate_diversity_indices(data):
    results = {
        'Sample': [],
        'Simpson_Index': [],
        'Pielous_Evenness': []
    }

    for column in data.columns[1:]:
        # Extracting the abundances for the sample
        abundances = data[column].values
        total = abundances.sum()

        # Simpson Index Calculation
        simpson_index = 1 - np.sum((abundances / total) ** 2)

        # Shannon Index (needed for Pielou's Evenness)
        shannon_index = entropy(abundances, base=np.e)

        # Pielou's Evenness
        max_shannon_index = np.log(len(abundances))
        pielous_evenness = shannon_index / max_shannon_index if max_shannon_index > 0 else np.nan

        # Append results
        results['Sample'].append(column)
        results['Simpson_Index'].append(simpson_index)
        results['Pielous_Evenness'].append(pielous_evenness)

    return pd.DataFrame(results)

# File paths for the datasets
file_paths = {
    '37week_CHOICE': '/mnt/data/37week_CHOICE.csv',
    '37week_CONV': '/mnt/data/37week_CONV.csv',
    '31week_CHOICE': '/mnt/data/31week_CHOICE.csv',
    '31week_CONV': '/mnt/data/31week_CONV.csv'
}

# Process each file
for dataset_name, file_path in file_paths.items():
    # Load the data
    data = pd.read_csv(file_path)

    # Calculate the diversity indices
    diversity_indices = calculate_diversity_indices(data)

    # Save the results to a CSV file
    diversity_indices.to_csv(f'/mnt/data/{dataset_name}_DiversityIndices.csv', index=False)
