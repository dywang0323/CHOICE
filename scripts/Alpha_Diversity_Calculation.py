import pandas as pd
import numpy as np

# Function to calculate Shannon Diversity Index
def shannon_diversity_index(values):
    """ Calculate the Shannon Diversity Index. """
    # Normalizing the values to probabilities
    probabilities = values / values.sum()
    # Shannon Diversity Index formula
    return -np.sum(probabilities * np.log(probabilities))

# Load the data
file_path = '/path/to/your/file.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Dropping the 'clade_name' column for calculation
diversity_data = data.drop(columns='clade_name')

# Calculating Richness and Shannon Diversity Index for each column
richness = diversity_data.count()
shannon_diversity = diversity_data.apply(shannon_diversity_index)

# Creating a DataFrame to display the results
diversity_results = pd.DataFrame({'Richness': richness, 'Shannon Diversity Index': shannon_diversity})
