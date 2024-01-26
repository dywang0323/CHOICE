library(tidyverse)
library(lme4)
library(glmmTMB)
library(readr)
library(caret)

# Ensure all necessary packages are installed and loaded
if (!requireNamespace("Matrix", quietly = TRUE)) install.packages("Matrix")
if (!requireNamespace("lattice", quietly = TRUE)) install.packages("lattice")

# Read the metadata
metadata <- read_csv("/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Input/Metadata_infant.csv")

# List the files (or subsets) to analyze
# Replace with the actual path where the subset files are stored
files <- list.files(path = "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Input/test/Infant_subset", full.names = TRUE, pattern = "\\.csv$")

# Loop over each file/subset
for (file in files) {
  # Read the data
  data_infant <- read_csv(file)

  # Assuming the last column is the response variable (cluster)
  response_var <- names(data_infant)[ncol(data_infant)]
  names(data_infant)[ncol(data_infant)] <- "response"

  # Merge the metadata and the cluster data
  data_merge <- inner_join(data_infant, metadata, by = 'Subject_ID')

  # Pre-processing
  data_merge <- data_merge %>%
    filter(!is.na(response)) %>%
    mutate(response = as.numeric(response))

  # Select variables for the model
  fixed_effects <- setdiff(names(data_merge), c('Sample_ID', 'response', 'Subject_ID'))

  # Convert all variables to numeric for correlation check
  data_merge_for_cor <- select(data_merge, all_of(fixed_effects)) %>%
    mutate_if(is.character, as.factor) %>% 
    mutate_if(is.factor, as.numeric)

  # Remove columns with zero standard deviation
  data_merge_for_cor <- data_merge_for_cor %>%
    select_if(~sd(.) != 0)

  # Check for multicollinearity
  cor_matrix <- cor(data_merge_for_cor, use = "complete.obs")
  highly_correlated <- findCorrelation(cor_matrix, cutoff = .75)
  data_merge <- select(data_merge, -all_of(names(highly_correlated)))

  # Manually exclude variables if they exist in the dataset
  columns_to_exclude <- c('BreastFeeding_2Mo', 'BreastFeeding_4Mo', 'Samp_2Week', 'Samp_2Month')
  existing_columns_to_exclude <- columns_to_exclude[columns_to_exclude %in% names(data_merge)]
  data_merge <- select(data_merge, -all_of(existing_columns_to_exclude))

  # Update fixed effects after removing correlated predictors and manually excluded columns
  fixed_effects <- setdiff(names(data_merge), c('Sample_ID', 'response', 'Subject_ID'))

  # Construct GLMM formula
  glmm_formula <- as.formula(paste("response ~", paste(fixed_effects, collapse = " + "), "+ (1 | Subject_ID)"))

  # Fit GLMM model
  glmm_model <- glmmTMB(glmm_formula, data = data_merge, family = nbinom2)
  model_summary <- summary(glmm_model)

  # Initialize the result data frame with total reads
  result <- data.frame(Total_Reads = sum(data_merge$response))

  # Add the number of subjects
  result$No_Subjects <- model_summary$ngrps$cond

  # Add the number of observations
  result$No_Observations <- model_summary$nobs

  # Handle coefficients
  coefficients <- model_summary$coefficients$cond
  col_names <- apply(expand.grid(rownames(coefficients), colnames(coefficients)), 1, paste, collapse = "_")
  coefficients <- t(as.data.frame(as.vector(coefficients)))
  colnames(coefficients) <- col_names
  result <- cbind(result, coefficients)

  # Add sigma
  result$Sigma <- model_summary$sigma

  # Add AICtab
  result <- cbind(result, t(model_summary$AICtab))

  # Writing the result
  output_filename <- paste("/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Input/test/subset_results/GLMM_", response_var, ".csv", sep = "")
  write.csv(result, output_filename, row.names = FALSE)
}
