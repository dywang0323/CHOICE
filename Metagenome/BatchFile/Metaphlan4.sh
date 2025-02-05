#!/bin/bash

#SBATCH --partition=32gb_20core
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --exclusive
#SBATCH --mem=30G
#SBATCH --job-name=submit_metaphlan
#SBATCH --output=CHOICE_submit_%J_stdout.txt
#SBATCH --error=CHOICE_submit_%J_stderr.txt
#SBATCH --mail-user=dywang@ou.edu
#SBATCH --mail-type=ALL
#SBATCH --chdir=/scratch/dywang/

# Enable error handling
set -euo pipefail

# Define directories
INPUT_DIR="/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/PREPROCESS/EC_M_time"
OUTPUT_DIR="/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/metaphlan/Mother_0204"
BOWTIE2_DB="/ourdisk/hpc/prebiotics/dywang/Software/metaphlan_databases"
BOWTIE2_OUT_DIR="/scratch/dywang/Metaphlan/Mother"
INDEX_NAME="mpa_vOct22_CHOCOPhlAnSGB_202212"

# Create necessary directories if they don't exist
mkdir -p "$OUTPUT_DIR"
mkdir -p "$BOWTIE2_OUT_DIR"

echo "Starting MetaPhlAn job submission at $(date)"

# Loop through each .fq.gz file in the input directory
for INPUT_FILE in ${INPUT_DIR}/*.fq.gz; do
    # Extract the base name (e.g., CHO13B from CHO13B.fq.gz)
    BASE_NAME=$(basename "$INPUT_FILE" .fq.gz)

    # Define a unique SLURM job script for this dataset
    JOB_SCRIPT="run_metaphlan_${BASE_NAME}.sh"

    # Define output file paths
    OUTPUT_FILE="${OUTPUT_DIR}/${BASE_NAME}.txt"
    BOWTIE2_OUT="${BOWTIE2_OUT_DIR}/${BASE_NAME}.bowtie2.bz2"

    # Create the SLURM job script
    cat <<EOF > $JOB_SCRIPT
#!/bin/bash
#SBATCH --partition=32gb_20core
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --exclusive
#SBATCH --mem=30G
#SBATCH --job-name=metaphlan_${BASE_NAME}
#SBATCH --output=${OUTPUT_DIR}/${BASE_NAME}_%J_stdout.txt
#SBATCH --error=${OUTPUT_DIR}/${BASE_NAME}_%J_stderr.txt
#SBATCH --mail-user=dywang@ou.edu
#SBATCH --mail-type=ALL
#SBATCH --chdir=/scratch/dywang/

echo "Processing file: $INPUT_FILE at $(date)"

metaphlan "$INPUT_FILE" \\
    --input_type fastq \\
    --bowtie2db "$BOWTIE2_DB" \\
    -x "$INDEX_NAME" \\
    --add_viruses \\
    -t rel_ab_w_read_stats \\
    -o "$OUTPUT_FILE" \\
    --bowtie2out "$BOWTIE2_OUT" \\
    --nproc 20

echo "Completed processing: $INPUT_FILE | Output saved to: $OUTPUT_FILE at $(date)"
EOF

    # Submit the job script
    sbatch "$JOB_SCRIPT"

    echo "Submitted job for $INPUT_FILE | SLURM script: $JOB_SCRIPT"

done

echo "All MetaPhlAn jobs submitted at $(date)!"
