# module load R/3.6.2-foss-2019b

# Load necessary libraries
library('DESeq2')
library('ggplot2')
library('ggrepel')

# File paths
countsName <- "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/Deseq/summarized_infant.txt" # Replace with your actual file path
metaDataName <- "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/Deseq/MetaData.txt" # Replace with your actual file path

# Read count data and metadata
countData <- read.table(countsName, header = TRUE, sep = "\t", stringsAsFactors = F)
metaData <- read.table(metaDataName, header = TRUE, sep = "\t", row.names = 1)

# Check if sample names in countData and metaData match
sampleNames <- colnames(countData)[-1] # Exclude the first column (Cluster)
if (!all(sampleNames %in% rownames(metaData))) {
  stop("Sample names in countData and metaData do not match")
}

# Filter out genes/clusters with zero counts across all samples
countData <- countData[rowSums(countData[,-1]) > 0,]

# Adding a small pseudo-count (e.g., 1) to all counts
countData[,-1] <- countData[,-1] + 1

# Creating DESeqDataSet
dds <- DESeqDataSetFromMatrix(countData = countData[, -1], 
                              colData = metaData, 
                              design = ~ dex)

# Running DESeq
dds <- DESeq(dds)

# Extracting and saving results
res <- results(dds)
res <- res[order(res$padj),]
write.table(res, "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/Deseq/compare_cluster_infant.txt", quote = F)

# PCA Plot
vsdata <- varianceStabilizingTransformation(dds, blind = TRUE)
pdf("/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/Deseq/PCA_plot.pdf")
plotPCA(vsdata, intgroup = "dex")
dev.off()

# Volcano Plot
res$threshold <- factor(ifelse(res$padj < 0.05 & abs(res$log2FoldChange) >= 1, 
                               ifelse(res$log2FoldChange >= 1, 'Up', 'Down'), 'NoSignificant'), 
                        levels = c('Up', 'Down', 'NoSignificant'))

pdf("/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Clustering/Deseq/Volcano_plot.pdf")
ggplot(res, aes(x = log2FoldChange, y = -log10(pvalue))) +
  geom_point(aes(color = threshold)) +
  geom_vline(xintercept = c(-1, 1), linetype = "dashed") +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed") +
  theme_classic() +
  labs(title = "Volcano plot", x = "Log2 Fold Change", y = "-Log10 p-value")
dev.off()
