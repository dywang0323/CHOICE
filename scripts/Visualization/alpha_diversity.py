import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def preprocess_data(file_path):
    # Load the file into a DataFrame
    df = pd.read_csv(file_path)

    # Perform necessary preprocessing, like combining 'Time_Point' and 'Group'
    df['Combined_Group'] = df['Time_Point'] + '_' + df['Group']
    
    return df

def save_plot_as_tif(data, index_name, title, group_order, colors, file_name, directory):
    plt.clf()
    fig, ax = plt.subplots(figsize=(12, 6))

    # Drawing the half-violin plots and other plot elements
    # ... [Include the full plot drawing code from the previous example here]

    # Save the plot as a .tif file with 300 dpi resolution
    file_path = os.path.join(directory, f'{file_name}.tif')
    plt.savefig(file_path, format='tif', dpi=300, bbox_inches='tight')
    plt.close()

    return file_path

# Directory containing your files
directory = 'path_to_your_directory'

# Assuming the structure of the files is similar and they have the same columns
group_order_corrected = ['31week_CONV', '31week_CHOICE', '37week_CONV', '37week_CHOICE']
colors_corrected = {
    '31week_CONV': 'skyblue', 
    '31week_CHOICE': 'lightgreen', 
    '37week_CONV': 'lightcoral', 
    '37week_CHOICE': 'mediumpurple'
}

# Loop through each file in the directory
for file_name in os.listdir(directory):
    if file_name.endswith('.csv'):
        file_path = os.path.join(directory, file_name)

        # Preprocess the data
        data_df = preprocess_data(file_path)

        # Create plots for each index
        for index in ['Simpson_Index', 'Pielous_Evenness']:
            plot_title = f'{index} by Group and Time Point'
            save_file_name = file_name.replace('.csv', f'_{index}')
            save_plot_as_tif(data_df, index, plot_title, group_order_corrected, colors_corrected, save_file_name, directory)
