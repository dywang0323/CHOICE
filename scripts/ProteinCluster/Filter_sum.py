# This script is used for filtering out the cluster that contain less than 3 subject and sum up the protein counts of each cluster

import pandas as pd

def filter_and_summarize_clusters(input_file_path, output_file_path):
    # Read the CSV file
    data = pd.read_csv(input_file_path)

    # Extracting the subject IDs from the second column
    data['Subject_ID'] = data.iloc[:, 1].apply(lambda x: x.split('_')[0])

    # Grouping by Cluster and counting unique subject IDs
    cluster_subject_count = data.groupby(data.columns[0])['Subject_ID'].nunique()

    # Filtering clusters with more than 3 unique subject IDs
    clusters_to_keep = cluster_subject_count[cluster_subject_count > 2].index
    filtered_data = data[data[data.columns[0]].isin(clusters_to_keep)]

    # Summing up the values for each cluster
    cluster_sums = filtered_data.groupby('Cluster').sum()

    # Removing rows where all values are 0
    cluster_sums = cluster_sums.loc[(cluster_sums != 0).any(axis=1)]

    # Converting to integers
    # Be sure that the data contains no NaNs and is appropriate for integer conversion
    cluster_sums = cluster_sums.round(0).astype(int)

    # Saving the summarized data to a new CSV file
    cluster_sums.to_csv(output_file_path)

    return cluster_sums

# Example usage
input_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/Infant_Cluster.csv'
output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/summarized_infant.csv'
summarized_data = filter_and_summarize_clusters(input_file_path, output_file_path)

# Optionally, you can print the summarized data
print(summarized_data.head())  # Displaying the first few rows of the summarized data
