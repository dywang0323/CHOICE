import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

def calculate_bray_curtis_matrices(dataset1, dataset2):
    # Align the species (rows) in both datasets
    dataset2_aligned = dataset2.set_index('clade_name').reindex(dataset1['clade_name']).fillna(0).reset_index()
    # Compute Bray-Curtis distances between all pairs of samples (one from each dataset)
    bc_distances = cdist(dataset1.drop('clade_name', axis=1).T, dataset2_aligned.drop('clade_name', axis=1).T, metric='braycurtis')
    return bc_distances

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

    # Calculate Bray-Curtis distances
    bc_matrices = calculate_bray_curtis_matrices(dataset1, dataset2)

    # Save the results to CSV files
    for i, column in enumerate(dataset1.columns[1:]):
        pd.DataFrame({f'{dataset2_name}_Sample': dataset2.columns[1:],
                      'Bray_Curtis_Distance': bc_matrices[i]}).to_csv(f"{time_point}_{column}_Bray_Curtis_Distances.csv", index=False)

print("Processing complete.")
