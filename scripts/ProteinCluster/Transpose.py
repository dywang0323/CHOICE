import pandas as pd

# Define the path to the input .clstr file
file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Fromated_Maternal.clstr'

# Read the .clstr file into a dataframe, assuming it is tab-separated
data = pd.read_csv(file_path, sep='\t')

# Split the 'Proteins' column by commas to separate each protein
data['Proteins'] = data['Proteins'].str.split(',')

# Function to format the cluster and its proteins
def format_cluster(cluster_id, proteins):
    formatted_text = f">{cluster_id}\n" + "\n".join(proteins)
    return formatted_text

# Applying the formatting function to each row
formatted_clusters = [format_cluster(row['clusterID'], row['Proteins']) for index, row in data.iterrows()]

# Joining all formatted clusters into a single text string
formatted_data = "\n".join(formatted_clusters)

# Define the path for the output text file
output_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/ClusterPro_M.txt'

# Save the formatted data to a text file
with open(output_path, 'w') as file:
    file.write(formatted_data)

print(f"Formatted data saved to {output_path}")
