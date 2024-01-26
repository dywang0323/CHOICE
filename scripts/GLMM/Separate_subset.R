library(tidyverse)

# Read the data (Replace with your actual file path)
data <- read_csv("/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Input/Infant_Cluster_glmm_2.csv")

# Assuming the first two columns are to be retained in all subsets
first_two_columns <- data[1:2]

# Identify cluster columns
# Adjust the pattern as per your actual column names
# Example pattern here is "Cluster_", change it if your cluster columns are named differently
cluster_columns <- grep("Cluster_", names(data), value = TRUE)

# Create and store subsets in a list
list_of_subsets <- list()

for (cluster in cluster_columns) {
  # Create a subset with first two columns and the current cluster column
  subset_data <- cbind(first_two_columns, data[cluster])
  
  # Naming the subset based on the cluster name and storing it in the list
  list_of_subsets[[cluster]] <- subset_data
}

# Now 'list_of_subsets' contains all your subsets
# Each subset is named after each cluster

# Optional: Write each subset to a separate CSV file
for (name in names(list_of_subsets)) {
  write_csv(list_of_subsets[[name]], paste0("/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Input/test/", name, ".csv"))
}
