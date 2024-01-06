# This script is used to run GLMM on the data of infant
# Include needed packages
library("tidyverse")
library("glmm")
library("lme4")

# Read the data of infant of one cluster
data_infant <- read.table("C:/Users/drzuy/OneDrive/Desktop/GLMM/Infant_test/Cluster_2_GLMM_infant.txt", quote="\"", comment.char="")
# Name the columns
colnames(data_infant) <- c("Subject_ID", "Sample_ID", "response")

# Read the data of metadata_infant 
metadata <- read.csv("C:/Users/drzuy/OneDrive/DeskTop/GLMM/Infant_test/Metadata_infant.csv", header= TRUE)

# Merge the metadata and the cluster data
data_merge <- merge(data_infant, metadata, by='Subject_ID')

# Remove rows with NA in column response
data_merge <- data_merge %>% drop_na()
# Round each number in column response
data_merge$response <- round(data_merge$response)

# Get all variables
all_variables <- colnames(data_merge)
# Get mixed effects
mixed_effects <- all_variables[-which(all_variables == c('Sample_ID'))]
mixed_effects <- mixed_effects[-which(mixed_effects == c('response'))]
# Get fixed effects
fixed_effects <- mixed_effects[-which(mixed_effects == c('Subject_ID'))]
# Check unique values of each column and remove the variable that has only one value
for(feature in fixed_effects){
  print(length(unique(data_merge[,feature])))
  if(length(unique(data_merge[,feature]))==1){
    fixed_effects <- fixed_effects[-which(fixed_effects == feature)]
  }
}

# Run GLMM
# GLMM formula
glmm_formula <- paste("response", paste(paste(fixed_effects, collapse="+"), '(1|Subject_ID)', sep='+'), sep="~")
glmm_formula <- as.formula(glmm_formula)
# GLMM model
glmm_model <- glmer(formula=glmm_formula, family = poisson(link='log'), data = data_merge)
summary(glmm_model)
