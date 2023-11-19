from scipy.stats import mannwhitneyu

# Separate the alpha diversity values for control and treatment groups
control_alpha_diversity = alpha_diversity_long[alpha_diversity_long['Group'] == 'Control_Group']['AlphaDiversity']
treatment_alpha_diversity = alpha_diversity_long[alpha_diversity_long['Group'] == 'Treatment_Group']['AlphaDiversity']

# Perform Mann-Whitney U Test
u_statistic, p_value = mannwhitneyu(control_alpha_diversity, treatment_alpha_diversity, alternative='two-sided')

# Clear the figure to start fresh for the new plot with p-value
plt.clf()

# Set up the matplotlib figure again
fig, ax = plt.subplots(figsize=(8, 6))

# Drawing the half-violin plots
for group in group_order:
    # Select the data for the group
    group_data = alpha_diversity_long[alpha_diversity_long['Group'] == group]
    # Draw the violin plot
    sns.violinplot(x='Group', y='AlphaDiversity', data=group_data,
                   color=colors[group], scale='width', inner=None, bw=0.2, cut=0, linewidth=2, order=group_order, ax=ax)
    
    # Modify the violin plots to keep only the right half
    for violin in ax.collections[-1::len(group_order)]:  # Adjust the collection selection
        violin.set_facecolor('none')  # Remove fill
        violin.set_edgecolor(colors[group])
        # Get the path of the violin
        violin_path = violin.get_paths()[0]
        vertices = violin_path.vertices
        # Keep only the right half of the violin plot
        median = np.median(vertices[:, 0])
        vertices[:, 0] = np.clip(vertices[:, 0], median, np.max(vertices[:, 0]))

# Overlay box plots with the same color as the violins and no fill
for group in group_order:
    group_data = alpha_diversity_long[alpha_diversity_long['Group'] == group]
    sns.boxplot(x='Group', y='AlphaDiversity', data=group_data, order=group_order,
                showcaps=False, boxprops={'facecolor':'None', 'edgecolor':colors[group]},
                whiskerprops={'color':colors[group]}, medianprops={'color':colors[group]}, 
                zorder=10, width=0.1, linewidth=2, ax=ax)

# Add jitter plot with larger dots in the specified colors and increased border size
sns.stripplot(x='Group', y='AlphaDiversity', data=alpha_diversity_long, order=group_order,
              jitter=True, dodge=True, marker='o', alpha=1, size=7, edgecolor='black', 
              linewidth=2, palette=colors, ax=ax)  # Increased border size here

# Annotate the p-value on the plot
y_max = alpha_diversity_long['AlphaDiversity'].max()
ax.text(0.5, y_max, 'p-value = {:.3f}'.format(p_value), horizontalalignment='center', size=14)

# Adjust the y-axis to have a proper range and labels
ax.set_ylim(y_min - 0.1, y_max + 0.2)  # Adjust ylim to make space for the p-value
ax.yaxis.set_major_locator(plt.MaxNLocator(4))

# Set the correct x-axis labels
ax.set_xticklabels(['Control', 'Treatment'])

# Remove spines and set title and labels
sns.despine()
ax.set_title('Alpha Diversity: Control vs Treatment')
ax.set_xlabel('')
ax.set_ylabel('Alpha Diversity')

# Define the file path for the updated TIFF output with p-value
updated_final_plot_path_with_pvalue = '/mnt/data/alpha_diversity_final_plot_with_pvalue.tif'

# Save the updated figure as a TIFF file with 300 dpi resolution
plt.savefig(updated_final_plot_path_with_pvalue, format='tif', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

(updated_final_plot_path_with_pvalue, p_value)
