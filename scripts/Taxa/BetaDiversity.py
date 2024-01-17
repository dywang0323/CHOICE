import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from scipy.stats import mannwhitneyu

def calculate_average_distances(dataset1, dataset2):
    # Align the species (rows) in both datasets
    dataset2_aligned = dataset2.set_index('clade_name').reindex(dataset1['clade_name']).fillna(0).reset_index()
    # Compute Bray-Curtis distances between all pairs of samples (one from each dataset)
    bc_distances = cdist(dataset1.drop('clade_name', axis=1).T, dataset2_aligned.drop('clade_name', axis=1).T, metric='braycurtis')
    # Calculate the average distance for each sample in dataset1
    average_distances = bc_distances.mean(axis=1)
    return average_distances

def mann_whitney_test(dataset1, dataset2):
    # Ensure the species (rows) in both datasets are aligned
    dataset2_aligned = dataset2.set_index('clade_name').reindex(dataset1['clade_name']).fillna(0).reset_index()
    # Perform Mann-Whitney U test for each pair of corresponding columns
    p_values = []
    for col1, col2 in zip(dataset1.columns[1:], dataset2_aligned.columns[1:]):  # Skip 'clade_name' column
        u_statistic, p_value = mannwhitneyu(dataset1[col1], dataset2_aligned[col2], alternative='two-sided')
        p_values.append(p_value)
    return p_values

# Define your dataset pairs and time points
time_points = ["2month", "4month", "2week", "31week", "37week"]
conditions = ["CHOICE", "CONV"]

# Process each dataset pair
for time_point in time_points:
    dataset1_name = f"{time_point}_{conditions[0]}"  # e.g., "2month_CHOICE"
    dataset2_name = f"{time_point}_{conditions[1]}"  # e.g., "2month_CONV"

    # Load the datasets
    dataset1 = pd.read_csv(f"{dataset1_name}.csv")
    dataset2 = pd.read_csv(f"{dataset2_name}.csv")

    # Calculate average Bray-Curtis distances
    average_distances = calculate_average_distances(dataset1, dataset2)

    # Perform Mann-Whitney U test for p-values
    p_values = mann_whitney_test(dataset1, dataset2)

    # Save the results to CSV files
    pd.DataFrame({'Sample': [f"{dataset1_name}_Sample{i}" for i in range(1, len(average_distances) + 1)],
                  'Average_Bray_Curtis_Distance': average_distances}).to_csv(f"{time_point}_Average_Bray_Curtis_Distances.csv", index=False)
    
    pd.DataFrame({'Sample': [f"{dataset1_name}_Sample{i}" for i in range(1, len(p_values) + 1)],
                  'P_Value': p_values}).to_csv(f"{time_point}_Mann_Whitney_U_p_values.csv", index=False)

print("Processing complete.")
