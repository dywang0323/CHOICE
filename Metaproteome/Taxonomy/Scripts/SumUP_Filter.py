# This script is used for summing up the protein abundance based on the genus, then filtering out the records that the prevalence is lower than 5%

import pandas as pd

# Load datasets
kaiju_file = "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Kaiju/Mother/Kaiju_GENUS_PRO_Mother.csv"  # Update with your full dataset filename
metadata_file = "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Kaiju/Mother/MetaData_Maternal_V6.csv"

# Read CSV files
kaiju_df = pd.read_csv(kaiju_file)
metadata_df = pd.read_csv(metadata_file)

# Extract genus name from "Taxa" column (removing numerical TaxID and semicolon)
kaiju_df["Genus"] = kaiju_df["Taxa"].str.split("_").str[1].str.replace(";", "", regex=True)

# Drop unnecessary columns (keeping only numerical data and genus, excluding "Protein ID")
numerical_cols = [col for col in kaiju_df.columns if col not in ["Taxa", "Protein ID", "Genus"]]
genus_abundance = kaiju_df.groupby("Genus")[numerical_cols].sum().reset_index()

# Map Sample_ID to Group (CONV or CHOICE)
sample_to_group = metadata_df.set_index("Sample_ID")["Group"].to_dict()

# Identify sample columns for each group
conv_samples = [s for s in numerical_cols if sample_to_group.get(s) == "CONV"]
choice_samples = [s for s in numerical_cols if sample_to_group.get(s) == "CHOICE"]

# Compute prevalence (% of nonzero samples per group)
genus_abundance["Prevalence_CONV"] = (genus_abundance[conv_samples] > 0).sum(axis=1) / len(conv_samples) * 100
genus_abundance["Prevalence_CHOICE"] = (genus_abundance[choice_samples] > 0).sum(axis=1) / len(choice_samples) * 100

# Filter genera with at least 5% prevalence in EITHER CONV or CHOICE (not both)
filtered_genus_abundance = genus_abundance[
    (genus_abundance["Prevalence_CONV"] >= 5) | (genus_abundance["Prevalence_CHOICE"] >= 5)
]

# Save filtered data
output_file = "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Kaiju/Mother/Kaiju_Genus_sum_filter_0217.csv"
filtered_genus_abundance.to_csv(output_file, index=False)

print(f"Filtered results saved to {output_file}")
