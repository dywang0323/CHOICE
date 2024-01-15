import os
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Directory containing your datasets
directory = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/metaphlan/Species/'

# Read and concatenate all datasets in the directory
dataframes = []
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        df['Dataset'] = filename.split('.')[0]  # Add a column to indicate the source dataset
        dataframes.append(df)

# Combine all dataframes
combined_data = pd.concat(dataframes, ignore_index=True)

# Preprocessing
combined_data = combined_data.drop(columns=['clade_name']).fillna(0)
dataset_labels = combined_data['Dataset']
combined_data = combined_data.drop(columns=['Dataset'])
scaler = StandardScaler()
data_normalized = scaler.fit_transform(combined_data)

# t-SNE Analysis
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
tsne_results = tsne.fit_transform(data_normalized)

# Create a DataFrame for the t-SNE results
tsne_df = pd.DataFrame(tsne_results, columns=['TSNE1', 'TSNE2'])
tsne_df['Dataset'] = dataset_labels

# Define a custom color palette
color_map = {
    '2week_CHOICE': 'blue',
    '2week_CONV': 'lightblue',
    '2month_CHOICE': 'green',
    '2month_CONV': 'lightgreen',
    '4month_CHOICE': 'grey',
    '4month_CONV': 'lightgrey',
    '31week_CHOICE': 'red',
    '31week_CONV': 'orange',
    '37week_CHOICE': '#ffc8dd',
    '37week_CONV': 'yellow'
}

# Map the dataset labels to colors
tsne_df['color'] = tsne_df['Dataset'].map(color_map)

# Plotting
plt.figure(figsize=(16, 10))
for dataset in tsne_df['Dataset'].unique():
    subset = tsne_df[tsne_df['Dataset'] == dataset]
    plt.scatter(subset['TSNE1'], subset['TSNE2'], label=dataset, color=color_map[dataset], alpha=0.7)

plt.title('t-SNE Results Colored by Dataset', fontsize=20)
plt.xlabel('TSNE1', fontsize=14)
plt.ylabel('TSNE2', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Add a legend
plt.legend(loc='best', fontsize=12, title='Datasets')

plt.savefig('tsne_results.pdf', dpi=300, format='pdf')
plt.savefig('tsne_results.tif', dpi=300, format='tif')

plt.show()
