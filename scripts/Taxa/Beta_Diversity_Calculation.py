from sklearn.metrics import pairwise_distances
import pandas as pd

# Function to calculate Bray-Curtis Dissimilarity
def bray_curtis_dissimilarity(matrix):
    """ Calculate the Bray-Curtis dissimilarity matrix. """
    # The pairwise_distances function can calculate Bray-Curtis dissimilarity
    return pairwise_distances(matrix.T, metric='braycurtis')

# Assuming 'diversity_data' is loaded as shown in the alpha diversity script
# Calculating the Bray-Curtis dissimilarity matrix
bray_curtis_matrix = bray_curtis_dissimilarity(diversity_data.fillna(0))

# Converting the matrix to a DataFrame for better readability
bray_curtis_df = pd.DataFrame(bray_curtis_matrix, 
                              index=diversity_data.columns, 
                              columns=diversity_data.columns)
