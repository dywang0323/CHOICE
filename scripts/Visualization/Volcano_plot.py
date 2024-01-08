import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
tpm_data = pd.read_csv('/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/ReadMapping/Deseq_CAZy/Com_CAZy_M_time.txt', sep='\t')
length_data = pd.read_csv('/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/ReadMapping/Deseq_CAZy/Deseq/Com_CAZy_B_time.txt', sep='\t')

# Define thresholds for significance
padj_threshold = 0.05
log2fc_threshold = 1

# Identify significant changes in TPM data
significant_tpm = tpm_data[(tpm_data['padj'] < padj_threshold) & (abs(tpm_data['log2FoldChange']) > log2fc_threshold)]

# Identify significant changes in Length data
significant_length = length_data[(length_data['padj'] < padj_threshold) & (abs(length_data['log2FoldChange']) > log2fc_threshold)]

# Identifying IDs with significant increase and decrease in HBEC_Length data
increase_ids_length = set(significant_length[significant_length['log2FoldChange'] > log2fc_threshold]['ID'])
decrease_ids_length = set(significant_length[significant_length['log2FoldChange'] < -log2fc_threshold]['ID'])

# Prepare data for plotting
tpm_data['-log10(padj)'] = -np.log10(tpm_data['padj'])
tpm_data['Color'] = 'grey'  # Default color for non-significant changes
tpm_data['Marker'] = 'o'    # Default filled circle marker for all points
tpm_data['EdgeColor'] = 'none'  # Default edge color for all points

# Applying color coding for significant changes in TPM data
tpm_data.loc[(tpm_data['padj'] < padj_threshold) & (tpm_data['log2FoldChange'] < -log2fc_threshold), 'Color'] = 'darkblue'  # Significant decrease
tpm_data.loc[(tpm_data['padj'] < padj_threshold) & (tpm_data['log2FoldChange'] > log2fc_threshold), 'Color'] = 'red'    # Significant increase

# Applying diamond shape with edge colors for IDs significant in HBEC_Length
tpm_data.loc[tpm_data['ID'].isin(increase_ids_length), ['Marker', 'EdgeColor']] = ['D', 'orange']  # Diamond shape with orange edge for increase
tpm_data.loc[tpm_data['ID'].isin(decrease_ids_length), ['Marker', 'EdgeColor']] = ['D', 'lightblue']  # Diamond shape with light blue edge for decrease

# Create the adjusted volcano plot with specified markers, colors, and edge colors
plt.figure(figsize=(6, 6))

# Plotting each category separately
for marker in ['o', 'D']:  # Filled circles and diamonds
    for color in ['red', 'darkblue', 'grey']:
        for edge_color in ['none', 'orange', 'lightblue']:
            subset = tpm_data[(tpm_data['Marker'] == marker) & (tpm_data['Color'] == color) & (tpm_data['EdgeColor'] == edge_color)]
            if marker == 'D' and edge_color != 'none':
                plt.scatter(subset['log2FoldChange'], subset['-log10(padj)'], 
                            edgecolors=edge_color, facecolors='none', alpha=0.7, marker=marker, s=50)  # Unfilled diamond with edge color
            else:
                plt.scatter(subset['log2FoldChange'], subset['-log10(padj)'], 
                            color=color, alpha=0.7, marker=marker)  # Filled circle

# Title and labels
plt.title('CAZymes materanl VS. infant')
plt.xlabel('Log2 Fold Change')
plt.ylabel('-Log10(Adjusted P-Value)')

# Adding threshold lines
plt.axhline(y=-np.log10(padj_threshold), color='gray', linestyle='--')
plt.axvline(x=log2fc_threshold, color='gray', linestyle='--')
plt.axvline(x=-log2fc_threshold, color='gray', linestyle='--')

# Save the plot as PDF and TIFF with 300 DPI
plt.savefig('volcano_plot.pdf', format='pdf', dpi=300)
plt.savefig('volcano_plot.tif', format='tiff', dpi=300)

plt.show()
